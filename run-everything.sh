#!/bin/bash

set -eux

./for-each-project.sh ./get-project.sh  # checkout all projects and build them
./run-mutations.sh
./create-classifier.sh
