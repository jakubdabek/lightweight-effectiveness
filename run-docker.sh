#!/bin/bash

set -eux

DOCKER_USER=${DOCKER_USER-ubuntu}
PROJECTS_VOLUME="pbr-lightweight-projects"
m2_VOLUME="pbr-lightweight-m2"
RESULTS_VOLUME="pbr-lightweight-results"
image="pbr-lightweight"

"${DOCKER-docker}" run --rm \
    -v "${PROJECTS_VOLUME}:/home/${DOCKER_USER}/experiments/projects" \
    -v "${m2_VOLUME}:/home/${DOCKER_USER}/.m2" \
    -v "${RESULTS_VOLUME}:/home/${DOCKER_USER}/experiments/results" \
    -it "$image";
