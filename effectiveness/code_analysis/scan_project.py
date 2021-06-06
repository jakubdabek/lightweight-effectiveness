import logging
import os
import re
import subprocess
from collections import OrderedDict
from pathlib import Path
from typing import List, Optional, Tuple

import pandas as pd
import glob
from effectiveness.code_analysis.get_commit import get_last_commit_id
from effectiveness.code_analysis.pom_module import CutPair, PomModule
from effectiveness.pom_utils import ET, POM_NSMAP
from effectiveness.settings import PROJECTS_DIR, SCAN_PROJECT_DIR, RESULTS_DIR, TSDETECT_JAR, TSDETECT_DIR

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


def search_project_tests(project_path: Path, results_dir=SCAN_PROJECT_DIR):
    submodules = get_submodules(project_path)

    if submodules:
        submodule_cuts = {}
        for submodule in submodules:
            submodule_path = project_path / submodule
            cuts = search_module_tests(
                project_path,
                project_path.name,
                submodule_path,
                submodule,
                results_dir=results_dir,
            )
            submodule_cuts[submodule] = cuts

        total_tests = sum(len(cuts) for cuts in submodule_cuts.values())
        print(f"Total tests for {project_path.name}: {total_tests}")
        for submodule, cuts in submodule_cuts.items():
            print(f"   - {submodule}: {len(cuts)}")
    else:
        search_module_tests(
            project_path, project_path.name, project_path, results_dir=results_dir
        )


def search_module_tests(
    project_path: Path,
    project_name: str,
    module_path: Path,
    module_name: str = None,
    results_dir=SCAN_PROJECT_DIR,
) -> List[CutPair]:
    """Scan a project and save CUTs with their tests to a file"""

    pom = module_path / 'pom.xml'
    if not pom.exists():
        return []

    if module_name:
        full_name = f"{project_name}/{module_name}"
    else:
        full_name = project_name

    print(f"* Scanning {full_name}")

    print(f"* * Found pom: {pom}")

    tree = ET.parse(pom)
    root = tree.getroot()

    include_patterns = []
    exclude_patterns = []

    surefire_plugin = root.find(
        ".//pom:plugin/[pom:artifactId='maven-surefire-plugin']", POM_NSMAP
    )
    if surefire_plugin is None:
        if module_path != project_path:
            print("* * * Couldn't find maven-surefire-plugin in pom")
            print("* * * Searching parent pom")
            parent_pom = project_path / 'pom.xml'
            if parent_pom.exists():
                print(f"* * * Found parent pom: {parent_pom}")
                surefire_plugin = (
                    ET.parse(parent_pom)
                    .getroot()
                    .find(".//pom:plugin/[pom:artifactId='maven-surefire-plugin']", POM_NSMAP)
                )

    if surefire_plugin is None:
        print("* * * Couldn't find maven-surefire-plugin in any pom")
    else:
        print("* * maven-surefire-plugin found")
        includes = surefire_plugin.findall('.//pom:include', POM_NSMAP)
        for include in includes:
            include_patterns.append(include.text)
        excludes = surefire_plugin.findall('.//pom:exclude', POM_NSMAP)
        for exclude in excludes:
            exclude_patterns.append(exclude.text)

    DEFAULT_INCLUDES = [
        "**/*Test.java",
        "**/Test*.java",
        "**/*Tests.java",
        "**/*TestCase.java",
    ]

    print("* * Found include patterns:", include_patterns)

    if not include_patterns:
        include_patterns = DEFAULT_INCLUDES
    else:
        for i in reversed(range(len(include_patterns))):
            pat = include_patterns[i]
            if pat.endswith("AllTests.java"):
                # TODO: parse AllTests.java
                print("* * * AllTests.java file found in includes!")
                if len(include_patterns) == 1:
                    include_patterns = DEFAULT_INCLUDES
                    break
                else:
                    del include_patterns[i]

    include_patterns = list(set(include_patterns))
    print("* * Adjusted include patterns:", include_patterns)

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

    print("* * Main path:", main_path)
    print("* * Tests path:", tests_path)

    # TODO: remove duplicate test entries
    test_pairs = list(module.find_cut_pairs(tests_path, main_path))

    print(f"* *  -  {full_name}: Found {len(test_pairs)} class-test pairs")

    cut_pairs_to_csv(test_pairs, module_path, module, results_dir)

    # TODO: move to separate file
    pairs_to_tsdetect_csv(test_pairs, project_name, results_dir)
    generate_tsdetect_csv(project_name)
    merge_testsmells()

    return test_pairs


def generate_tsdetect_csv(project_name):
    #                                    /experiments/results/scan_project/tsDetect/{project_name}.csv
    print("Detecting smells with tsdetect")
    print(f"\njava -jar {TSDETECT_JAR} {RESULTS_DIR}/scan_project/tsDetect_{project_name}.csv\n")
    os.system(f"java -jar {TSDETECT_JAR} {RESULTS_DIR}/scan_project/tsDetect_{project_name}.csv")
    os.system(f"mv TsDetect_{project_name}.csv /home/ubuntu/experiments/effectiveness/tsDetect/projects/TsDetect_{project_name}.csv")


def pairs_to_tsdetect_csv(test_pairs: List[CutPair], projectName, output=TSDETECT_DIR):
    project = [projectName] * len(test_pairs)
    path_test = [test_pair.test_path for test_pair in test_pairs]
    path_src = [test_pair.source_path for test_pair in test_pairs]
    frame = pd.DataFrame(
        OrderedDict(
            (
                ('project', project),
                ('path_test', path_test),
                ('path_src', path_src)
            )
        )
    )
    output = output /f"tsDetect_{projectName}.csv"
    print("** Saving output for tsDetect to", output)
    frame.to_csv(output, index=False, header=False)


def merge_testsmells(dir=TSDETECT_DIR):
    print("merging tsDetext csvs")
    print(dir)
    all_files = glob.glob(dir.__str__() + "/projects/*.csv")
    out_file = []
    for filename in all_files:
        current_file = pd.read_csv(filename, index_col=None, header=0)
        out_file.append(current_file)
    
    frame = pd.concat(out_file, axis=0, ignore_index=True)
    frame.to_csv(dir / "test-smells.csv", index=False)
    print("done merging")


def cut_pairs_to_csv(
    test_pairs: List[CutPair],
    module_path: Path,
    module: PomModule,
    output=SCAN_PROJECT_DIR,
):
    last_commit = get_last_commit_id(module_path)
    project = [module.project_name] * len(test_pairs)
    module_col = [module.name] * len(test_pairs)
    test_path = [test_pair.test_path for test_pair in test_pairs]
    test_name = [test_pair.test_qualified_name for test_pair in test_pairs]
    class_path = [test_pair.source_path for test_pair in test_pairs]
    src_name = [test_pair.source_qualified_name for test_pair in test_pairs]
    frame = pd.DataFrame(
        OrderedDict(
            (
                ('project', project),
                ('module', module_col),
                ('commit', last_commit),
                ('test_path', test_path),
                ('test_name', test_name),
                ('class_path', class_path),
                ('class_name', src_name),
            )
        )
    )

    old_output = output / f"res_{module.name}.csv"

    latest = output / module.project_name / "latest"
    output = output / module.project_name / last_commit
    output.mkdir(exist_ok=True, parents=True)
    if not latest.is_symlink() and latest.is_dir():
        import shutil

        shutil.rmtree(latest)
    latest.unlink(missing_ok=True)
    latest.symlink_to(output.relative_to(latest.parent), target_is_directory=True)

    filename = f"tests_{module.name or module.project_name}.csv"

    print("* * Saving CUTs to", output / filename)
    frame.to_csv(old_output, index=False)
    frame.to_csv(output / filename, index=False)


def load_cut_pairs(path: Path) -> Optional[Tuple[str, str, List[CutPair]]]:
    """Loads CUT data from `path`

    Returns:
        (project_name, module_name, list_of_cuts)
        or None if there's no data
    """

    data = pd.read_csv(path)
    if data.empty:
        return None

    project = data["project"].unique()
    assert len(project) == 1, f"{path} should contain data for one project"
    module = data["module"].fillna('').unique()
    assert len(module) == 1, f"{path} should contain data for one module"

    return (
        project[0],
        module[0],
        [
            CutPair(test_path, test_qualified_name, source_path, source_qualified_name)
            for test_path, test_qualified_name, source_path, source_qualified_name in data[
                ["test_path", "test_name", "class_path", "class_name"]
            ].itertuples(index=False)
        ],
    )


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
