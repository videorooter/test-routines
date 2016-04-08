#! /usr/bin/python3
"""
This is a utility script which read Internet Archive identifiers on
stdin and for each identifier, looks up the metadata and downloads the
original source.
"""
import fileinput
import urllib.error
import json
import requests
from urllib.request import urlopen

wanted_formats = {"movies":['Ogg Video', 'MPEG2', 'MPEG4'],
                  "image":['PNG', 'gif', 'JPEG']}
outputdir = 'data/'
max_accuracy_files = 5
max_total_files = 10000
# max_total_files = 10

num_files = {"image":0, "movies":0}

for line in fileinput.input():
  (format, id) = line.strip().split()
  if num_files[format] >= max_total_files:
     continue
  print("Considering %s (%s)\r" % (id, format), end='')
  try:
     response = requests.get('https://archive.org/metadata/%s' % id)
  except:
     continue
  data = response.json()

  for i in data['files']:
     # We only want original works in the format we require. They should
     # not be set to private, and the filename should not contain additional
     # directory paths.
     if i['source'] == 'original' and i['format'] in wanted_formats[format] and ('private' not in i or i['private'] != 'true') and '/' not in i['name']:
        url = 'http://%s%s/%s' % (data['server'], data['dir'], i['name'])
        try:
           print("Downloading %s (%s bytes)\r" % (i['name'], i['size']), end='')
           response_dl = urlopen(url)
        except:
           print("FAIL: %s" % line)
           continue
        else:
           if num_files[format] < max_accuracy_files:
              (base, ext) = i['name'].split('.')
              filename = "%s/%s/0/%03d.%s" % (outputdir, format, num_files[format], ext)
           elif num_files[format] < max_total_files:
              filename = "%s/%s/lg/%s" % (outputdir, format, i['name'])
           else:
              break
           with open(filename, 'b+w') as f:
             f.write(response_dl.read())
           print("OK: %s (as %s, format %s)" % (id, i['name'], i['format']))
           num_files[format] += 1
           break
