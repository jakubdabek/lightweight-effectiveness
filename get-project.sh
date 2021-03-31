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
git checkout --force "$commit"

# maven doesn't support java version 1.5 anymore
sed -i -E 's/(<[^>]*(:?target|source)>)1.5/\11.6/' pom.xml
# maven repositories must be accessed through https
sed -i -E 's/http:\/\/(repo[^<]*maven)/https:\/\/\1maven/' pom.xml

mvn clean install -DskipTests
mvn test -Dmaven.test.failure.ignore.true
