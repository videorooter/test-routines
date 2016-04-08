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

echo "`date` Removing leftover information"
#rm -r data/

echo "`date` Creating source directories in data/"
mkdir -p data/{movies,image}/0
mkdir -p data/{movies,image}/lg

echo "`date` Downloading sets"
cat sources/internetarchive.id.txt|./utility/internetarchive-downloader.py
