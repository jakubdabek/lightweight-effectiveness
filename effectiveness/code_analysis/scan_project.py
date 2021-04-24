import logging
import os
import re
import subprocess
from collections import OrderedDict
from pathlib import Path
from typing import List, Optional, Tuple

import pandas as pd
from effectiveness.code_analysis.get_commit import get_last_commit_id
from effectiveness.code_analysis.pom_module import CutPair, PomModule
from effectiveness.pom_utils import ET, POM_NSMAP
from effectiveness.settings import PROJECTS_DIR, RESULTS_DIR

special_cases = {
    'core': ('/src/', '/test/'),
    'guava': ('/src/', '/guava-tests/test/'),
    'guava-gwt': ('/src/', '/test/'),
}


def get_submodules(project_path: Path) -> List[str]:
    """
    Analyzes the structure of the project and detect whether more modules are present

    Returns:
    list of submodules
    """
    pom_path = project_path / 'pom.xml'
    assert pom_path.exists()
    pom_parsed = ET.parse(pom_path)
    modules = pom_parsed.find('pom:modules', POM_NSMAP)
    modules_list = []
    if modules:
        for module in modules.findall('pom:module', POM_NSMAP):
            detected_module = module.text
            if 'xml' not in detected_module:
                modules_list.append(detected_module)
    logging.info(f'Found {len(modules_list)} module(s):\n', modules_list)

    return modules_list


def search_project_tests(project_path: Path, results_dir=RESULTS_DIR):
    submodules = get_submodules(project_path)

    if submodules:
        for submodule in submodules:
            submodule_path = project_path / submodule
            search_module_tests(project_path.name, submodule_path, submodule, results_dir=results_dir)
    else:
        search_module_tests(project_path.name, project_path, results_dir=results_dir)


def search_module_tests(
    project_name: str,
    module_path: Path,
    module_name: str = None,
    results_dir=RESULTS_DIR,
) -> List[CutPair]:
    """Scan a project and save CUTs with their tests to a file"""

    pom = module_path / 'pom.xml'
    if not pom.exists():
        return []

    if module_name:
        print(f"** Scanning {project_name}/{module_name}")
    else:
        print(f"** Scanning {project_name}")

    print(f"** Found pom: {pom}")

    tree = ET.parse(pom)
    root = tree.getroot()

    include_patterns = []
    exclude_patterns = []

    surefire_plugin = root.find(
        ".//pom:plugin/[pom:artifactId='maven-surefire-plugin']", POM_NSMAP
    )
    if surefire_plugin is not None:
        print("** maven-surefire-plugin found")
        includes = surefire_plugin.findall('.//pom:include', POM_NSMAP)
        for include in includes:
            include_patterns.append(include.text)
        excludes = surefire_plugin.findall('.//pom:exclude', POM_NSMAP)
        for exclude in excludes:
            include_patterns.append(exclude.text)

    DEFAULT_INCLUDES = [
        "**/*Test.java",
        "**/Test*.java",
        "**/*Tests.java",
        "**/*TestCase.java",
    ]

    from pprint import pprint

    pprint(include_patterns)

    if not include_patterns:
        include_patterns = DEFAULT_INCLUDES
    else:
        for i, pat in enumerate(include_patterns):
            if re.fullmatch(".*/?AllTests.java$", pat):
                print("*** AllTests.java file found in includes, changing to *Test.java")
                include_patterns[i] = "**/*Test.java"

    include_patterns = list(set(include_patterns))
    pprint(include_patterns)

    source_directory, test_source_directory = get_source_directories(
        module_path,
        project_name,
        module_name,
    )

    module = PomModule(project_name, module_name, include_patterns, exclude_patterns)
    # special case for guava
    if project_name == 'guava' and not module_path.endswith('gwt'):
        tests_path = module_path.parent / test_source_directory
    else:
        tests_path = module_path / test_source_directory
    main_path = module_path / source_directory

    print("** Main path:", main_path)
    print("** Tests path:", tests_path)

    # TODO: remove duplicate test entries
    test_pairs = list(module.find_cut_pairs(tests_path, main_path))

    cut_pairs_to_csv(test_pairs, module_path, module, results_dir)

    return test_pairs


def cut_pairs_to_csv(
    test_pairs: List[CutPair],
    module_path: Path,
    module: PomModule,
    output=RESULTS_DIR,
):
    last_commit = get_last_commit_id(module_path)
    project = [module.project_name] * len(test_pairs)
    module_col = [module.name] * len(test_pairs)
    path_test = [test_pair.test_path for test_pair in test_pairs]
    test_name = [test_pair.test_qualified_name for test_pair in test_pairs]
    path_src = [test_pair.source_path for test_pair in test_pairs]
    src_name = [test_pair.source_qualified_name for test_pair in test_pairs]
    frame = pd.DataFrame(
        OrderedDict(
            (
                ('project', project),
                ('module', module_col),
                ('commit', last_commit),
                ('path_test', path_test),
                ('test_name', test_name),
                ('path_src', path_src),
                ('class_name', src_name),
            )
        )
    )

    old_output = output / f"res_{module.name}.csv"

    output2 = output / module.project_name / "latest"
    output = output / module.project_name / last_commit
    output.mkdir(exist_ok=True, parents=True)
    output2.mkdir(exist_ok=True, parents=True)

    # second parentheses empty if no submodule
    filename = f"tests({module.project_name})({module.name or ''}).csv"

    print("** Saving CUTs to", output)
    frame.to_csv(old_output, index=False)
    frame.to_csv(output / filename, index=False)
    frame.to_csv(output2 / filename, index=False)


def load_cut_pairs(path: Path) -> List[CutPair]:
    data = pd.read_csv(path)
    return [
        CutPair(test_path, test_qualified_name, source_path, source_qualified_name)
        for test_path, test_qualified_name, source_path, source_qualified_name in data[
            ["path_test", "test_name", "path_src", "class_name"]
        ].itertuples(index=False)
    ]


def get_source_directories(
    module_path: Path, project_name: str, module_name: str
) -> Tuple[str, str]:
    """Return the source and test source directory from the pom (or one of the poms)"""
    try:
        look_for = project_name if not module_name else module_name
        return special_cases[look_for]
    except KeyError:
        pass

    pom_paths = list(module_path.glob('pom*.xml'))

    override_source = look_for_tag(pom_paths, 'sourceDirectory', direct_children_of="build")
    override_test_source = look_for_tag(
        pom_paths, 'testSourceDirectory', direct_children_of="build"
    )

    # check the test dir and the source dir
    test_dir = 'src/test/java' if override_test_source is None else override_test_source
    test_dir = test_dir.strip('/')

    src_dir = 'src/main' if override_source is None else override_source
    src_dir = src_dir.strip('/')

    return src_dir, test_dir


def look_for_tag(
    poms: List[Path], tag: str, *, children_of: str = None, direct_children_of: str = None
) -> Optional[str]:
    """Return string content of a tag in one of the supplied poms"""
    for pom in poms:
        pom = ET.parse(pom).getroot()
        if children_of:
            pattern = f".//pom:{children_of}//pom:{tag}"
        elif direct_children_of:
            pattern = f".//pom:{direct_children_of}/pom:{tag}"
        else:
            pattern = f".//pom:{tag}"
        element = pom.find(pattern, POM_NSMAP)
        if element is not None:
            return re.sub("[$@*}?].*[$@*}?]", "", element.text)
    return None


if __name__ == '__main__':

    def main():
        from sys import argv, exit

        if len(argv) < 2:
            print(f"Error! Usage: {argv[0]} <project_path> [<result_path>]")
            exit(1)
        search_project_tests(*map(Path, argv[1:3]))

    main()
