from effectiveness.mutation.mutation_calc import calc_coverage
from effectiveness.mutation.pitest_html_parser import PitestHTMLParser, ParserOutput
from effectiveness.settings import RESULTS_DIR, MUTATION_RESULTS_DIR, METRICS_DIR, ALL_OPERATORS
from effectiveness.utils import tuple_if_none

import pandas as pd

from typing import Optional
import os

__author__ = "Giovanni Grano"
__license__ = "MIT"
__email__ = "grano@ifi.uzh.ch"


def calculate_results(operator, default_dir=RESULTS_DIR, clean=True, name='results'):
    """Aggregates all the mutations calculated and add the information about the mutation

    Arguments
    -------------
    :param default_dir: the dir where all the csv files are stores
    :param clean: flag to remove classes with no mutations
    :param name: the name of the output file
    """
    if not default_dir.is_dir():
        print("No dir to process! You're missing some previous steps")
        exit(1)

    result_csv = list(default_dir.glob('res_*.csv'))
    aggregate = pd.concat([pd.read_csv(project) for project in result_csv])

    current_mutation_results = MUTATION_RESULTS_DIR.with_name(MUTATION_RESULTS_DIR.name + '-' + operator)
    if not current_mutation_results.exists():
        print("* No results for", operator)
        return

    aggregate[['module']] = aggregate[['module']].fillna(value='')

    report_data = aggregate.apply(lambda row: tuple_if_none(parse_html_report(row, current_mutation_results), 3), axis=1, result_type='expand')
    aggregate[["total_mutations", "mutation_score", "line_coverage"]] = report_data

    if clean:
        print('Rows before the cleaning = {}'.format(aggregate.shape[0]))
        print('Projects:', aggregate['project'].unique().tolist())
        aggregate = aggregate.dropna()
        aggregate = aggregate[aggregate['total_mutations'] != 0]
        print('Rows after the cleaning = {}'.format(aggregate.shape[0]))
        print('Projects:', aggregate['project'].unique().tolist())
    filename = (METRICS_DIR / name).with_suffix('.csv')
    print(f"Saving to {filename}")
    aggregate.to_csv(filename, index=False)


def parse_html_report(row, path=MUTATION_RESULTS_DIR) -> Optional[ParserOutput]:
    """Get data about mutation results from PIT HTML report"""
    module_name = row.module
    if module_name == '':
        path = path / row.project / row.test_name
    else:
        path = path / row.project / (module_name + '-' + row.test_name)
    
    # find all reports in root folders of test runs
    report_files = list(path.glob('*/index.html'))
    if not report_files:
        # no file = no mutations
        return None
    
    # use the most recent file (alphabetically last)
    return PitestHTMLParser.parse(report_files[-1])


if __name__ == '__main__':
    def main():
        for operator in ALL_OPERATORS:
            calculate_results(operator, name='results-{}'.format(operator))
        # calculate_results()

    main()
