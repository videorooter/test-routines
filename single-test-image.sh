#! /bin/bash
#
# Run a single (image) test on a specific github repo and branch.
# Takes repo and branch as input.
#
repo=$1
branch=$2
sha=$3
sudo rm -rf src		# If exists
mkdir -p src data/log/

(cd src; git clone $1; cd *; git checkout $2)
pwd=`pwd`

cd utility/docker
sudo docker build -t cm/$sha .
sudo docker run -v $pwd/data/:/data:ro -v $pwd/src/:/src \
                -v $pwd/utility/:/util:ro \
                cm/$sha /util/docker-run-tests.sh $repo $branch

rm -rf src
