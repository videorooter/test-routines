#! /bin/bash
#
# This script is called automatically inside a Docker container
# on a standard Ubuntu host. It is called with exactly one argument:
# the github repository (and branch) to compile a blockhash from
# and to run tests against.
#
# The script can expect /data to hold the data directory from the host.
#

apt-get update
apt-get install git
apt-get install build-essential

