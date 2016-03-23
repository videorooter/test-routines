#! /bin/bash
#
cat <<_EOL_
WARNING: This script will download a LOT of data: upwards of 5,000
videos and 20,000 images. You should make sure you have enough disk
space to house this.

If you do not wish to do this: press Ctrl-C now.

(continuing automatically in 5 seconds)
_EOL_
sleep 5

echo "`date` Creating source directories in data/"
mkdir -p data/{videos,images}/0
mkdir -p data/{videos,images}/lg

echo "`date` Downloading small set (for accuracy testing)"
for i in images videos; do
  #
  # We step through the IA sources file and get the first 100
  # images or videos. If one of the downloads fail, we continue
  # with the next file in line, so that we get a total of 100
  # regardless of which download.
  #
  j=1  # Line number
  dest_dir="data/$i/0/"
  rm $dest_dir/*
  while test `ls $dest_dir|wc -l` -lt 5; do
    id=`sed "${j}q;d" sources/$i/internetarchive.id.txt`
    mkdir -p tmp
    (cd tmp; echo "$id"|../sources/_utility/internetarchive-downloader.py)
    if test ! -z "`ls tmp`"; then
      filename=`ls tmp|tail -1`
      last_n=`ls $dest_dir|sort|tail -1|cut -d'.' -f1`
      last_n=$((last_n+1))
      mv tmp/$filename data/$i/0/`printf "%03d" $last_n`.${filename##*.}
      rm -r tmp
    fi 
    j=$((j+1))
  done
done

