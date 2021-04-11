__author__ = "Giovanni Grano"
__license__ = "MIT"
__email__ = "grano@ifi.uzh.ch"

from effectiveness.mutation.project import CutPair, Module
from effectiveness.mutation.get_commit import get_last_commit_id
from effectiveness.mutation.utils import ET
from collections import OrderedDict
from effectiveness.settings import *
import subprocess
import logging

import os
import pandas as pd
import re

from typing import List, Tuple, Optional
from pathlib import Path


special_cases = {'core': ('/src/', '/test/'),
                 'guava': ('/src/', '/guava-tests/test/'),
                 'guava-gwt': ('/src/', '/test/')}


def get_submodules(project_path: Path):
    """
      Analyzes the structure of the project and detect whether more modules are present
      :param project_path the path of the project
      :return: a list of modules
      """
    pom_path = project_path / 'pom.xml'
    assert(pom_path.exists())
    pom_parsed = ET.parse(pom_path)
    modules = pom_parsed.find('pom:modules', POM_NSMAP)
    modules_list = []
    if modules:
        for module in modules.findall('pom:module', POM_NSMAP):
            detected_module = module.text
            if 'xml' not in detected_module:
                modules_list.append(detected_module)
    logging.info('Found {} module(s):\n'
                 '{}'.format(len(modules_list), modules_list))

    return modules_list


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

    surefire_plugin = root.find(".//pom:plugin/[pom:artifactId='maven-surefire-plugin']", POM_NSMAP)
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

    module = Module(project_name, module_name, include_patterns, exclude_patterns)
    # special case for guava
    if project_name == 'guava' and not module_path.endswith('gwt'):
        tests_path = module_path.parent / test_source_directory
    else:
        tests_path = module_path / test_source_directory
    main_path = module_path / source_directory

    print("** Main path:", main_path)
    print("** Tests path:", tests_path)

    test_pairs = list(module.find_cut_pairs(tests_path, main_path))

    cut_pairs_to_csv(test_pairs, module_path, module, results_dir)

    return test_pairs


def cut_pairs_to_csv(
    test_pairs: List[CutPair],
    module_path: Path,
    module: Module,
    output=RESULTS_DIR,
):
    last_commit = get_last_commit_id(module_path)
    project = [module.project_name] * len(test_pairs)
    module_col = [module.name] * len(test_pairs)
    path_test = [test_pair.test_path for test_pair in test_pairs]
    test_name = [test_pair.test_qualified_name for test_pair in test_pairs]
    path_src = [test_pair.source_path for test_pair in test_pairs]
    src_name = [test_pair.source_qualified_name for test_pair in test_pairs]
    frame = pd.DataFrame(OrderedDict((('project', project),
                                      ('module', module_col),
                                      ('path_test', path_test),
                                      ('test_name', test_name),
                                      ('path_src', path_src),
                                      ('class_name', src_name))))

    output = output / f"res_{module.project_name}.csv"

    # output2 = output / project.name / "latest"
    # output = output / project.name / last_commit
    # output.mkdir(exist_ok=True, parents=True)
    # output2.mkdir(exist_ok=True, parents=True)

    # if module.name is None:
    #     filename = f"tests+{module.project_name}.csv"
    # else:
    #     filename = f"tests+{module.project_name}+{module.name}.csv"

    print("** Saving CUTs to", output)
    frame.to_csv(output, index=False)
    # frame.to_csv(output2 / filename, index=False)


def get_source_directories(module_path: Path, project_name: str, module_name: str) -> Tuple[str, str]:
    """Return the source and test source directory from the pom (or one of the poms)"""
    try:
        look_for = project_name if not module_name else module_name
        return special_cases[look_for]
    except KeyError:
        pass

    pom_paths = list(module_path.glob('pom*.xml'))

    override_source = None  # look_for_tag(pom_paths, 'sourceDirectory', children_of="build")
    override_test_source = None  # look_for_tag(pom_paths, 'testSourceDirectory', children_of="build")

    # check the test dir and the source dir
    test_dir = 'src/test/java' if override_test_source is None else override_test_source
    test_dir = test_dir.strip('/')

    src_dir = 'src/main' if override_source is None else override_source
    src_dir = src_dir.strip('/')

    return src_dir, test_dir


def look_for_tag(poms: List[Path], tag: str, children_of: str = None) -> Optional[str]:
    """Return string content of a tag in one of the supplied poms"""
    for pom in poms:
        pom = ET.parse(pom).getroot()
        if children_of:
            pattern = f".//pom:{children_of}//pom:{tag}"
        else:
            pattern = f".//pom:{tag}"
        element = pom.find(pattern, POM_NSMAP)
        if element is not None:
            return re.sub("[$@*}?].*[$@*}?]", "", element.text)
    return None


if __name__ == '__main__':
    projects = ['cat']

    for project in projects:
        project_path = PROJECTS_DIR / project
        search_module_tests(project, project_path)
