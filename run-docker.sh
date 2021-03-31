set -eux

PROJECTS_VOLUME="pbr-lightweight-projects"
m2_VOLUME="pbr-lightweight-m2"
image="pbr-lightweight"

$DOCKER run --rm \
    -v "${PROJECTS_VOLUME}:/root/experiments/projects" \
    -v "${m2_VOLUME}:/root/.m2" \
    -it "$image";
