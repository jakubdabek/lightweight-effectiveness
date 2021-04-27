"""This module runs mutation tests on all given projects,
parses the results and saves them in convenient format.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List

import pandas as pd
from effectiveness import settings
from effectiveness.code_analysis.get_commit import get_last_commit_id
from effectiveness.code_analysis.pom_module import CutPair, PomModule
from effectiveness.code_analysis.scan_project import load_cut_pairs, search_project_tests
from effectiveness.mutation.pom_changer import add_pitest_plugin
from effectiveness.mutation.utils import get_projects
from effectiveness.utils import clear_dir


def main(projects: List[str], operator: str):
    # deal with directories
    settings.RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    clear_dir(settings.MUTATION_RESULTS_DIR)
    settings.MUTATION_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    clear_dir(settings.LOGS_DIR)
    settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)

    for i, project in enumerate(projects):
        print(f"* Running mutations for project {project} ({i}/{len(projects)})")
        run_project_mutations(project, operator)


def run_project_mutations(project: str, operator: str):
    # TODO: more logging
    project_path = settings.PROJECTS_DIR / project
    current_commit = get_last_commit_id(project_path)
    cuts_path = settings.SCAN_PROJECT_DIR / project / current_commit
    if not cuts_path.exists():
        search_project_tests(project_path)
        assert cuts_path.exists(), "search_project_tests should create the directory"

    results_path = settings.MUTATION_RESULTS_DIR / project / current_commit / operator
    results_path.mkdir(parents=True, exist_ok=True)

    for module_cuts in cuts_path.glob("tests_*.csv"):
        loaded = load_cut_pairs(module_cuts)
        if loaded is None:
            continue

        loaded_project, module, cut_tests = loaded
        assert loaded_project == project

        if module:
            module_path = project_path / module
        else:
            module_path = project_path

        run_module_mutations(
            project,
            module,
            project_path,
            module_path,
            results_path,
            cut_tests,
            operator,
        )


def run_module_mutations(
    project: str,
    module: str,
    project_path: Path,
    module_path: Path,
    results_path: Path,
    cut_tests: List[CutPair],
    operator: str,
):
    pom = module_path / "pom.xml"
    cached_pom = pom.with_name("~pom_cached.xml")
    print("* Caching original pom")
    shutil.copy2(pom, cached_pom)
    target = module_path / 'target'

    mutation_logs = settings.LOGS_DIR / project
    mutation_logs.mkdir(parents=True, exist_ok=True)
    try:
        for test in cut_tests:
            add_pitest_plugin(
                cached_pom,
                pom,
                class_to_mutate=test.source_qualified_name,
                test_to_run=test.test_qualified_name,
                mutator=operator,
            )
            print(f"* Mutating {test.source_qualified_name} with operator {operator}")
            subprocess.run(
                [
                    "mvn",
                    "org.pitest:pitest-maven:mutationCoverage",
                    "-X",
                    "-DoutputFormats=HTML",
                    "--log-file",
                    mutation_logs / f"{test.test_qualified_name}({module}).txt",
                ],
                cwd=module_path,
                timeout=settings.MUTATION_TIMEOUT,
                check=True,
            )

            tmp_target_dir = target / f"{test.test_qualified_name}({module})"
            if tmp_target_dir.exists():
                shutil.rmtree(tmp_target_dir)
            shutil.move(target / 'pit-reports', tmp_target_dir)
            shutil.copytree(
                tmp_target_dir, results_path / tmp_target_dir.name, dirs_exist_ok=True
            )
    finally:
        print("* Restoring pom.xml")
        pom.unlink()
        cached_pom.rename(pom)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("* Wrong usage!")
        print(f"* Usage: {sys.argv[0]} <csv_file_with_project_list.csv> [<operator>]")
        exit(1)

    projects_csv = sys.argv[1]
    projects = get_projects(projects_csv)

    operator = sys.argv[2] if len(sys.argv) >= 3 else "ALL"

    main(projects, operator)
