#!/bin/bash

set -eu

## This script requires data from mutations tests to be present (see run-everything.sh)

repeat-char() {
    printf "%*s" "$1" | tr " " "$2"
}

run-command() {
    title="$1"
    shift
    printf "%s %s %s\n" "$(repeat-char 30 '*')" "$title" "$(repeat-char 30 '*')"
    echo "[Press any key]"
    read -n1
    set -x
    "$@"
    set +x
}

# parse PIT output
run-command "Processing data" python3 effectiveness/mutation/calculate_results.py

# aggregate results of mutations and code metrics
run-command "Aggregating all data" python3 effectiveness/metrics/aggregate_sources.py

run-command "Creating classifier" python3 effectiveness/classification.py "median" "ALL"
