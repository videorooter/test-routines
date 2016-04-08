#! /bin/bash
#
# Run a single (image) test on a specific github repo and branch.
# Takes repo and branch as input.
#

cd utility/docker
sudo docker build --build-arg REPO=$1 --build-arg BRANCH=$2 .
# run -v data/:/data:ro
