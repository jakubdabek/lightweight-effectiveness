import os
from typing import Optional

import pandas as pd
from effectiveness.mutation.pitest_html_parser import ParserOutput, PitestHTMLParser
from effectiveness.settings import (
    ALL_OPERATORS,
    METRICS_DIR,
    MUTATION_RESULTS_DIR,
    RESULTS_DIR,
    SCAN_PROJECT_DIR,
)
from effectiveness.utils import tuple_if_none


def prepare_results(
    operator: str,
    *,
    mutation_results_dir=MUTATION_RESULTS_DIR,
    cuts_dir=SCAN_PROJECT_DIR,
    clean=True,
):
    """Aggregates mutation results into one data frame"""

    cut_files = cuts_dir.glob('*/latest/tests_*.csv')
    aggregate = pd.concat(map(pd.read_csv, cut_files))

    aggregate['module'].fillna('', inplace=True)

    report_data = aggregate.apply(
        lambda row: tuple_if_none(parse_html_report(row, operator, mutation_results_dir), 3),
        axis=1,
        result_type='expand',
    )
    aggregate[["total_mutations", "mutation_score", "line_coverage"]] = report_data

    if clean:
        print(f'Rows before cleaning = {aggregate.shape[0]}')
        print('Projects:', aggregate['project'].unique().tolist())
        aggregate = aggregate.dropna()
        aggregate = aggregate[aggregate['total_mutations'] != 0]
        print(f'Rows after cleaning = {aggregate.shape[0]}')
        print('Projects:', aggregate['project'].unique().tolist())

    filename = (METRICS_DIR / "mutation_reports" / operator).with_suffix('.csv')
    print(f"Saving to {filename}")
    aggregate.to_csv(filename, index=False)


def parse_html_report(row, operator, mutation_results_root) -> Optional[ParserOutput]:
    """Get data about mutation results from PIT HTML report"""
    path = mutation_results_root / row.project / row.commit / operator
    path = path / f"{row.test_name}({row.module})"

    # find all reports in root folders of test runs
    report_files = list(path.glob('*/index.html'))
    if not report_files:
        # no file = no mutations
        return None

    # use the most recent file (alphabetically last, because folder names are timestamps)
    return PitestHTMLParser.parse(report_files[-1])


if __name__ == '__main__':

    def main():
        for operator in ALL_OPERATORS:
            prepare_results(operator)
        # calculate_results()

    main()
