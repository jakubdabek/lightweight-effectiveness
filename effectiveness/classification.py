__author__ = "Giovanni Grano"
__email__ = "grano@ifi.uzh.ch"
__license__ = "MIT"

import warnings
import sys
from effectiveness.classification.classifier import classification


def warn(*args, **kwargs):
    """Used to suppress sklearn warnings"""
    pass


warnings.warn = warn


def main():
    """
    This script run the machine learning classifier.
    Whether you invoke the classification method without specified algorithm argument,
    the nested cross-validation process will compare all the possible algorithms specified
    and will give in output the results for the best one found in such a process.
    Whether you want to run the classification and get the results for a single algorithm,
    specify it through the algorithm argument.
    For the sake of simplicity, you might just de-comment one of the lines of code below.
    """

    suffix = sys.argv[1] if len(sys.argv) > 1 else ''

    if False:
        # full model
        N_INNER = 5
        N_OUTER = 10
        N_REPEATS = 10
    else:
        # faster classification
        N_INNER = 2
        N_OUTER = 3
        N_REPEATS = 2

    def run_classification(algorithm, consider_coverage):
        classification(
            consider_coverage=consider_coverage,
            n_inner=N_INNER,
            n_outer=N_OUTER,
            n_repeats=N_REPEATS,
            algorithm=algorithm,
            suffix=suffix,
        )

    # De-comment to run only the KNN algorithm
    # run_classification("knn", True)
    # run_classification("knn", False)

    # De-comment to run only the SVC algorithm
    # run_classification("svc", True)
    # run_classification("svc", False)

    # De-comment to run only the RFC algorithm
    run_classification("rfc", True)
    run_classification("rfc", False)

    # run_classification("all", True)
    # run_classification("all", False)


if __name__ == '__main__':
    main()
