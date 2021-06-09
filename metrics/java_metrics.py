import os
import subprocess
import csv

from pathlib import Path
from shutil import copy


JAVA_METRICS_JAR_NAME = 'java-metrics-1.0-SNAPSHOT-jar-with-dependencies.jar'
JAVA_METRICS_JAR_PATH = Path.cwd() / JAVA_METRICS_JAR_NAME
PROJECTS_DIR = Path.cwd() / 'projects'


def calculate_metrics(project: str):
    project_dir = PROJECTS_DIR / project

    # Skopiowanie jara do folderu projektu
    copy(JAVA_METRICS_JAR_PATH, project_dir)

    # Wyliczenie metryk
    if os.path.isfile(project_dir / 'results.csv'):
        os.remove(project_dir / 'results.csv')

    results_file = open(project_dir / 'results.csv', 'x', newline='')
    results_file_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    results_file_writer.writerow(['Project', 'Package', 'Class', 'MethodSignature', 'OuterClass', 'AccessModifier', 'IsStatic', 'IsFinal', 'ATFD', 'CA', 'CAM', 'CBO', 'CBOMZ', 'CE', 'CYCLO', 'DAM', 'DIT', 'LCOM', 'LD', 'LOC_C', 'LOC_M', 'MFA', 'MOA', 'MRD', 'NOAM', 'NOC', 'NOL_C', 'NOL_M', 'NOM', 'NOMM', 'NOMR_C', 'NOMR_M', 'NOPA', 'NOPV', 'NPM', 'RFC', 'WMC', 'WMCNAMM', 'WOC'])
    count_metrics(project_dir / 'src/main/java', project_dir, results_file_writer)
    results_file.close()

    if os.path.isfile(project_dir / 'output.csv'):
        os.remove(project_dir / 'output.csv')

    # Usunięcie jara z folderu projektu
    os.remove(project_dir / JAVA_METRICS_JAR_NAME)

    # Mergowanie wyników w głównym pliku java_metrics.csv
    if not os.path.isfile(Path.cwd() / 'metrics/java_metrics.csv'):
        main_results_file = open(Path.cwd() / 'metrics/java_metrics.csv', 'x', newline='')
        csv.writer(main_results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL).writerow(['Project', 'Package', 'Class', 'MethodSignature', 'OuterClass', 'AccessModifier', 'IsStatic', 'IsFinal', 'ATFD', 'CA', 'CAM', 'CBO', 'CBOMZ', 'CE', 'CYCLO', 'DAM', 'DIT', 'LCOM', 'LD', 'LOC_C', 'LOC_M', 'MFA', 'MOA', 'MRD', 'NOAM', 'NOC', 'NOL_C', 'NOL_M', 'NOM', 'NOMM', 'NOMR_C', 'NOMR_M', 'NOPA', 'NOPV', 'NPM', 'RFC', 'WMC', 'WMCNAMM', 'WOC'])
    else:
        main_results_file = open(Path.cwd() / 'metrics/java_metrics.csv', 'a', newline='')

    main_results_file_writer = csv.writer(main_results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    with open(project_dir / 'results.csv', 'rt') as f:
        data = csv.reader(f)
        for index, row in enumerate(data):
            if index != 0:
                main_results_file_writer.writerow(row)


def count_metrics(rootdir, project_dir, results_file_writer):
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            subprocess.run(
                ['java', '-jar', JAVA_METRICS_JAR_NAME, '-i', d],
                cwd=project_dir,
                shell=True
            )
            if os.path.isfile(project_dir / 'output.csv'):
                with open(project_dir / 'output.csv', 'rt') as f:
                    data = csv.reader(f)
                    for index, row in enumerate(data):
                        # print(f"{index}, {row}")

                        # Omijamy nagłówek i zapisujemy jedynie wiersze dotyczące całej klasy
                        if index != 0 and row[3] == '':
                            results_file_writer.writerow(row)
            count_metrics(d, project_dir, results_file_writer)
