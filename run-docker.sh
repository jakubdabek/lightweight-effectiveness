#!/bin/bash

set -eux

PROJECTS_VOLUME="pbr-lightweight-projects"
m2_VOLUME="pbr-lightweight-m2"
RESULTS_VOLUME="pbr-lightweight-results"
image="pbr-lightweight"

$DOCKER run --rm \
    -v "${PROJECTS_VOLUME}:/root/experiments/projects" \
    -v "${m2_VOLUME}:/root/.m2" \
    -v "${RESULTS_VOLUME}:/root/experiments/results" \
    -it "$image";
