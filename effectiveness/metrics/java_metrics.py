import csv
import subprocess
from pathlib import Path

from effectiveness.settings import METRICS_DIR, PROJECTS_DIR

JAVA_METRICS_JAR_NAME = 'java-metrics-1.0-SNAPSHOT-jar-with-dependencies.jar'
JAVA_METRICS_JAR_PATH = METRICS_DIR / JAVA_METRICS_JAR_NAME

JAVA_METRICS_COLUMNS = [
    'Project',
    'Package',
    'Class',
    'MethodSignature',
    'OuterClass',
    'AccessModifier',
    'IsStatic',
    'IsFinal',
    'ATFD',
    'CA',
    'CAM',
    'CBO',
    'CBOMZ',
    'CE',
    'CYCLO',
    'DAM',
    'DIT',
    'LCOM',
    'LD',
    'LOC_C',
    'LOC_M',
    'MFA',
    'MOA',
    'MRD',
    'NOAM',
    'NOC',
    'NOL_C',
    'NOL_M',
    'NOM',
    'NOMM',
    'NOMR_C',
    'NOMR_M',
    'NOPA',
    'NOPV',
    'NPM',
    'RFC',
    'WMC',
    'WMCNAMM',
    'WOC',
]


def calculate_metrics(project: str):
    project_dir = PROJECTS_DIR / project

    results_file_path = project_dir / 'results.csv'

    with open(results_file_path, 'w', newline='') as results_file:
        results_file_writer = csv.writer(
            results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        results_file_writer.writerow(JAVA_METRICS_COLUMNS)
        analyze_dir(project_dir / 'src/main/java', project_dir, results_file_writer)

    # Merge results to java_metrics.csv
    metrics_output = METRICS_DIR / 'java_metrics.csv'
    if not metrics_output.is_file():
        # create new file and write header
        metrics_output_file = open(metrics_output, 'w', newline='')
        csv.writer(
            metrics_output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL
        ).writerow(JAVA_METRICS_COLUMNS)
    else:
        # append rows to existing file
        metrics_output_file = open(metrics_output, 'a', newline='')

    with metrics_output_file:
        metrics_output_writer = csv.writer(
            metrics_output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        with open(project_dir / 'results.csv', 'rt') as f:
            data = csv.reader(f)
            next(data, None)  # omit header
            for row in data:
                metrics_output_writer.writerow(row)


def analyze_dir(rootdir: Path, project_dir: Path, results_writer):
    for subdir in rootdir.iterdir():
        if subdir.is_dir():
            subprocess.run(
                ['java', '-jar', JAVA_METRICS_JAR_PATH, '-i', subdir],
                cwd=project_dir,
            )
            output_file = project_dir / 'output.csv'
            if output_file.is_file():
                with open(output_file, 'r') as f:
                    data = csv.reader(f)
                    next(data, None)  # omit header
                    for row in data:
                        # use only rows that describe the whole class
                        if row[3] == '':
                            results_writer.writerow(row)
                output_file.unlink()
            analyze_dir(subdir, project_dir, results_writer)
