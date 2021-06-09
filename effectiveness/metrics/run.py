import sys
from typing import List

from effectiveness.metrics.checkstyle_metrics import (
    calculate_metrics as calculate_checkstyle_metrics,
)
from effectiveness.metrics.java_metrics import calculate_metrics as calculate_java_metrics
from effectiveness.mutation.utils import get_projects
from effectiveness.settings import METRICS_DIR
from effectiveness.utils import remove_file_if_exists


def calcutate_metrics(projects: List[str]):
    for i, project in enumerate(projects):
        print(f"* Calculating additional metrics for project {project} ({i + 1}/{len(projects)})")
        calculate_project_metrics(project)


def calculate_project_metrics(project: str):
    # Checkstyle
    # calculate_checkstyle_metrics(project)

    # JavaMetrics
    remove_file_if_exists(METRICS_DIR / 'java_metrics.csv')
    calculate_java_metrics(project)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("* Wrong usage!")
        print(f"* Usage: {sys.argv[0]} <csv_file_with_project_list.csv>")
        exit(1)

    projects_csv = sys.argv[1]
    projects = get_projects(projects_csv)

    calcutate_metrics(projects)
