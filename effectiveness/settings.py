from pathlib import Path
import os

MUTATION_TIMEOUT = 20 * 60  # 20m

# the base dir of the project
# all paths derived from this one will be absolute
BASE_DIR = Path(__file__).absolute().parent.parent

RUBY = '/Users/grano/.rvm/rubies/ruby-2.2.1/bin'

SCRIPT_READABILITY = BASE_DIR / 'metrics/readability/compute_readability.rb'

LOGS_DIR = BASE_DIR / 'logs'

# the directory that contains the data
DATA_DIR = BASE_DIR / 'data'

# directory containing the data frames to answer RQ1 (generated by the R script)
RQ1_DIR = DATA_DIR / 'rq1'

# the directory that contains the plots
PLOT_DIR = BASE_DIR / 'plots'

# the installation directory of Defect4j in the system
DEFECT4J = '/Users/grano/Documents/PhD/defects4j/framework/bin'

METRICS_DIR = BASE_DIR / 'metrics'

TSDETECT_DIR = METRICS_DIR / 'tsDetect'

# tsdetect jar
TSDETECT_JAR = TSDETECT_DIR / 'TestSmellDetector.jar'

# test smell jar
TEST_SMELL_JAR = METRICS_DIR / 'test-smells/test-smells.jar'

# code smell jar
CODE_SMELL_JAR = METRICS_DIR / 'code-quality/code-smells.jar'

# ck metrics jar
CK_METRICS_JAR = METRICS_DIR / 'code-quality/code-quality.jar'

# readability path
READABILITY_PATH = METRICS_DIR / 'readability'

# the path that contains the projects
PROJECTS_DIR = BASE_DIR / 'projects'

# the path of the Python package for the mutation
MUTATION_PACKAGE = BASE_DIR / 'effectiveness/mutation'

RESULTS_DIR = BASE_DIR / 'results'

SCAN_PROJECT_DIR = RESULTS_DIR / 'scan_project'

# the path that contains the mutation results
MUTATION_RESULTS_DIR = RESULTS_DIR / 'mutation'

PIT_VERSION = "1.3.2"
CHECKSTYLE_PLUGIN_VERSION = "3.1.2"

# PIT operators (https://pitest.org/quickstart/mutators/)
OPERATORS = {}

OPERATORS["DEFAULTS"] = [
    "CONDITIONALS_BOUNDARY",
    "INCREMENTS",
    "INVERT_NEGS",
    "MATH",
    "NEGATE_CONDITIONALS",
    "VOID_METHOD_CALLS",
]

OPERATORS["OLD_DEFAULTS"] = [
    *OPERATORS["DEFAULTS"],
    "RETURN_VALS",
]

OPERATORS["BETTER_RETURNS"] = [
    "TRUE_RETURNS",
    "FALSE_RETURNS",
    "PRIMITIVE_RETURNS",
    "EMPTY_RETURNS",
    "NULL_RETURNS",
]

OPERATORS["NEW_DEFAULTS"] = [
    *OPERATORS["DEFAULTS"],
    *OPERATORS["BETTER_RETURNS"],
]

OPERATORS["ALL"] = [
    *OPERATORS["NEW_DEFAULTS"],
    "REMOVE_CONDITIONALS",
    "EXPERIMENTAL_SWITCH",
    "INLINE_CONSTS",
    "CONSTRUCTOR_CALLS",
    "NON_VOID_METHOD_CALLS",
    "REMOVE_INCREMENTS",
]

ALL_OPERATORS = ["ALL", "NEW_DEFAULTS"] + OPERATORS["ALL"]
