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

wanted_formats = ['PNG', 'gif', 'JPEG', 'Ogg Video', 'MPEG2', 'MPEG4']

for line in fileinput.input():
  line = line.strip()
  response = requests.get('https://archive.org/metadata/%s' % line)
  if response.status_code != 200:
    print("FAIL: %s" % line)
    next

  data = response.json()

  for i in data['files']:
     if i['source'] == 'original' and i['format'] in wanted_formats and ('private' not in i or i['private'] != 'true'):
        url = 'http://%s%s/%s' % (data['server'], data['dir'], i['name'])
        try:
           response_dl = urlopen(url)
        except urllib.error.HTTPError:
           print("FAIL: %s" % line)
           response_dl = None
           next
        if response_dl is not None:
           with open(i['name'], 'b+w') as f:
             f.write(response_dl.read())
           print("OK: %s (as %s, format %s)" % (line.strip(), i['name'], i['format']))
