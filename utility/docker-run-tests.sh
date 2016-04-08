#! /bin/bash
#
# This script is called automatically inside a Docker container
# on a standard Ubuntu host. It is called with exactly two arguments:
# the github repository to compile a blockhash from
# and to run tests against, and the branch.
#
# The script can expect /data to hold the data directory from the host.
#

mkdir -p /compile
cd /compile
git clone $1
cd *

# echo "<h3>Repository: $1 (branch $2)</h3>"
git checkout $2 > /dev/null
if test -f waf; then
  (./waf configure;./waf) > /dev/null
elif test -f Makefile; then
  make > /dev/null
elif test -f prepare; then
  (./prepare; make) > /dev/null
else
  echo "Don't know how to compile $branch"
  exit 1
fi

