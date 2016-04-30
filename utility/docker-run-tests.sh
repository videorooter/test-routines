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

logfile=/src/output.html

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
  cat $$.in | /util/crosscompare.py --max 20 --step 1 --test "IMAGE" >> $logfile

  rm -f $$.in

  for img in `find /data/image/[0-9]* -maxdepth 3 -iregex '\(.*png\|.*jpg\)'|sort -f`; do  
    calc image $img >> $$.in
  done

  cat $$.in|/util/makecsv.py --max 20 --step 1 --verbatim 13 --test "IMAGE" >> $logfile
  rm -f $$.in
fi


if test $movies -eq 1; then
  #
  find /data/movies/lg -type f | while read img; do
    calc movie $img >> $$.in
  done

  #
  # Run the actual crosscompare for false positives and output
  # the results.
  
  cat $$.in | /util/crosscompare.py --test="MOVIE" >> $logfile

  rm -f $$.in

  for video in `find /data/movies/[0-9]* -maxdepth 4 -name "*.mpeg" -o \
                                      -name "*.avi" -o \
                                      -name "*.webm" -o \
                                      -name "*.mkv" -o \
                                      -name "*.ogv" | sort -f`; do
    calc movie $video >> $$.in
  done

  cat $$.in|/util/makecsv.py --verbatim 9 --test="MOVIE" >> $logfile
  rm -f $$.in
fi
