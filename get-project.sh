#!/bin/bash

set -eux

mkdir -p projects && cd projects

repo=$1
commit=$2
dir=$(echo "$repo" | cut -d'/' -f2)

if [ ! -d "$dir" ];
then
    git clone "https://github.com/$1" "$dir"
fi
cd "$dir"

git add -A --force
git reset --hard
git checkout --force "$commit"

for patch in "../../patches/$dir"/*.patch;
do
    if [ -f "$patch" ]
    then
        git apply "$patch"
    fi
done

# maven doesn't support java version 1.5 anymore
sed -i -E 's/(<[^>]*(:?target|source)>)1.5/\11.6/' pom.xml
# maven repositories must be accessed through https
sed -i -E 's/http:\/\/(repo[^<]*maven)/https:\/\/\1/' pom.xml

# additional/exceptional parameters to maven command based on project
case "$dir"
in
    # skip python module in OpenGrok
    opengrok) additional=(-pl \!opengrok-tools) ;;
    # empty array in the default case
    *) additional=() ;;
esac
# mvn clean install -DskipTests
mvn -e --update-snapshots clean test -Dmaven.test.failure.ignore=true "${additional[@]}"
