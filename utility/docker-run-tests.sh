#! /bin/bash
#
# This script is called automatically inside a Docker container
# on a standard Ubuntu host. It is called with exactly two arguments:
# the github repository to compile a blockhash from
# and to run tests against, and the branch.
#
# The script can expect /data to hold the data directory from the host.
#

cd /src/*
source videorooter.conf

echo "<h3>Repository: $1 (branch $2)</h3>"

compile

if test $images -eq 1; then
  #
  # For each file in the large data set of images, we compile the
  # hash and add it to a temporary table.
  #
  find /data/image/lg -type f | while read img; do
    calc image $img >> $$.in
  done

  #
  # Run the actual crosscompare for false positives and output
  # the results.
  #
  cat $$.in | /util/crosscompare.py --max 15 --step 1

  rm -f $$.in

  for img in `find /data/image/[1-9]* -maxdepth 3 -iregex '\(.*png\|.*jpg\)'|sort -f`; do  
    calc image $img >> $$.in
  done

  cat $$.in|/util/makecsv.py
  rm -f $$.in
fi
