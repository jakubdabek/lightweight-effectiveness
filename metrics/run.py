import sys
from typing import List
from pathlib import Path

import utils
from effectiveness.mutation.utils import get_projects
from metrics.checkstyle_metrics import calculate_metrics as calculate_checkstyle_metrics
from metrics.java_metrics import calculate_metrics as calculate_java_metrics


def calcutate_metrics(projects: List[str]):
    for i, project in enumerate(projects):
        print(f"* Calculating additional metrics for project {project} ({i + 1}/{len(projects)})")
        calculate_project_metrics(project)


def calculate_project_metrics(project: str):
    # Checkstyle
    # calculate_checkstyle_metrics(project)

    # JavaMetrics
    utils.remove_file_if_exists(Path.cwd() / 'metrics/java_metrics.csv')
    calculate_java_metrics(project)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("* Wrong usage!")
        print(f"* Usage: {sys.argv[0]} <csv_file_with_project_list.csv>")
        exit(1)

    projects_csv = sys.argv[1]
    projects = get_projects(projects_csv)

    calcutate_metrics(projects)
