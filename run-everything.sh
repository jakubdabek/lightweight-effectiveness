#!/bin/bash

set -eux

./for-each-project.sh ./get-project.sh  # checkout all projects and build them
python3 effectiveness/mutation/run.py projects.csv ALL  # run mutations
./create-classifier.sh
