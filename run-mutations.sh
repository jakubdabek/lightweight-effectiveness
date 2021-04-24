#!/bin/bash

set -eux

./make-runner.sh  # generate script for running mutations
./run_experiment_ALL.sh  # run mutations (by default with ALL operators)
