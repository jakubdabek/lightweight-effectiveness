#!/bin/bash

set -eu

csv_field() {
    echo "$1" | cut -d',' -f${2:-1}
}

export -f csv_field

script=$1
shift

tail -n+2 projects.csv | xargs -I'{}' bash -c "$script "'"$(csv_field "{}" 1)" "$(csv_field "{}" 2)"'" $(printf '%q ' "$@")" \; \
    || { echo "******* Errors while running $script *********"; exit 1; }
