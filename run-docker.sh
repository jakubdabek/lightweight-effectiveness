#!/bin/bash

set -eux
VOLUMES_SUFFIX="${VOLUMES_SUFFIX-''}"
DOCKER_USER=${DOCKER_USER-ubuntu}
PROJECTS_VOLUME="pbr-lightweight-projects${VOLUMES_SUFFIX}"
m2_VOLUME="pbr-lightweight-m2${VOLUMES_SUFFIX}"
RESULTS_VOLUME="pbr-lightweight-results${VOLUMES_SUFFIX}"
image="pbr-lightweight"

"${DOCKER-docker}" run --rm \
    -v "${PROJECTS_VOLUME}:/home/${DOCKER_USER}/experiments/projects" \
    -v "${m2_VOLUME}:/home/${DOCKER_USER}/.m2" \
    -v "${RESULTS_VOLUME}:/home/${DOCKER_USER}/experiments/results" \
    -it "$image";
