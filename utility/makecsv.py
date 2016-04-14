#! /usr/bin/env python
from __future__ import division

import os
import sys
import base64

def hammingdistance(x, y):
    return sum(bin(i^j).count("1") for i,j in zip(x,y))

table = {}

data = sys.stdin.readlines()

for d in data:
    d = d.strip()
    h, d = d.split(' ', 1)

    filename = os.path.basename(d)
    dirname = os.path.dirname(d)
    dirname = dirname.split('/', 1)[1] # strip prepared/
    print("Working with %s and %s-" % (filename, dirname))
    if dirname not in table:
        table[dirname] = {}

    if filename not in table[dirname]:
        # orig hash, hamming distances for method 1
        table[dirname][filename] = [None, None]

    if filename == "000.png":
        table[dirname][filename][0] = bytearray(base64.b16decode(h.strip().upper()))
    table[dirname][filename][1] = hammingdistance(table[dirname]['000.png'][0], bytearray(base64.b16decode(h.strip().upper())))

cols = table.keys()
cols.sort()

rows = table[cols[0]].keys()
rows.sort()

# First get statistics for row 1-13, ie all verbatim transformations
total = 0
l10 = 0
verbatim = {}
deriv = {}
for i in range(0, 16):
  verbatim[i] = 0
  deriv[i] = 0

for row in rows[:13]:
    for col in cols:
        total += 1
        value = table[col][row][1]
        for i in range(0, 16):
           if (value <= i):
              verbatim[i] += 1

# Second get statistics for row 14-25, ie all non-verbatim transformations
total_s = 0
for row in rows[13:]:
    for col in cols:
        total_s += 1
        value = table[col][row][1]
        for i in range(0, 16):
           if (value <= i):
              deriv[i] += 1

for i in range(0, 16):
   print " t=%d  Verbatim: %.2f%% Derivatives: %.2f%%" % (i, verbatim[i]*100/(total), deriv[i]*100/(total_s))

