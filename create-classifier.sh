#!/bin/bash

set -eux

## This script requires data from mutations tests to be present (see run-mutations.sh)

echo "******************** Processing data *******************" && read -n1
python3 effectiveness/mutation/calculate_results.py  # parse PIT output
echo "******************** Stage done *******************" && read -n1
python3 effectiveness/metrics/aggregate_sources.py  # aggregate results of mutations and code metrics
echo "******************** Stage done *******************" && read -n1
python3 effectiveness/classification.py "median" "ALL"
