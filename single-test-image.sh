#! /bin/bash
#
# Run a single (image) test on a specific github repo and branch.
# Takes repo and branch as input.
#
repo=$1
branch=$2
sudo rm -rf src		# If exists
mkdir -p src
(cd src; git clone $1; cd *; git checkout $2)
rev=`(cd src/*; git log -1 --pretty=%H)`
key=`echo $repo:$branch:$rev|md5sum|cut -d' ' -f1`
pwd=`pwd`

cd utility/docker
sudo docker build -t cm/$key .
sudo docker run -v $pwd/data/:/data:ro -v $pwd/src/:/src \
                -v $pwd/utility/:/util:ro \
                cm/$key /util/docker-run-tests.sh $repo $branch

rm -rf src
