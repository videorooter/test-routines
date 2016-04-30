#! /usr/bin/env python
from __future__ import division

import os
import sys
import base64
import argparse
import csv

def hammingdistance(x, y):
    return sum(bin(i^j).count("1") for i,j in zip(x,y))

parser = argparse.ArgumentParser(description='Accuracy comparison')
parser.add_argument('--max', default=50, type=int,
                   help='maximum hamming distance')
parser.add_argument('--step', default=5, type=int,
                   help='hamming distance step')
parser.add_argument('--verbatim', default=10, type=int,
                   help='number of test are verbatim tests')
parser.add_argument('--test', default="IMAGE",
                   help='name of the test (if any)')

args = parser.parse_args()

table = {}

data = sys.stdin.readlines()

print("Calculating accuracy...")

for d in data:
    d = d.strip()
    h, d = d.split(' ', 1)

    filename = os.path.basename(d)
    filename = int(filename.split('.')[0])
    dirname = os.path.dirname(d)
    testname = int(dirname.split('/')[3]) # strip data/X/

    if testname not in table:
        table[testname] = {}
    if testname == 0:
        table[testname][filename] = bytearray(base64.b16decode(h.strip().upper()))
    else:
        if filename in table[0]:
           table[testname][filename] = hammingdistance(table[0][filename], bytearray(base64.b16decode(h.strip().upper())))

# Cols is the individual test names
cols = table.keys()
cols.sort()

# Rows is the file names
rows = table[cols[0]].keys()
rows.sort()

writer = csv.writer(sys.stdout, delimiter='|', escapechar='\\', quoting=csv.QUOTE_NONE)
print("\n * %s Hamming distance overview (rows = testcases, cols=files, rows x cols = hamming distance to original)\n" % args.test)
rdata = []
rdata.append("%2s " % "")
for col in range(1, len(rows)):
   rdata.append("%4s" % str(col))
writer.writerow(rdata)
writer.writerow(['---'] + ['----'] * len(rows))

for row in range(1,len(cols)):
   rdata = []
   rdata.append("%2s " % row)
   for col in range(1, len(rows)):
      if col in table[row]:
         rdata.append("%4s" % table[row][col])
      else:
         rdata.append("%4s" % "-1")

   writer.writerow(rdata)

print("\n * %s Calculated accuracy results (set of %d videos)\n" % (args.test, len(rows)))

for t in range(0, args.max+1, args.step):
   match=0
   total=0
   inval=0
   for row in range(1,args.verbatim+1): # Only verbatim
      for col in range(1, len(rows)):
          if col in table[row]:
              if table[row][col] < t:
                 match += 1
              if table[row][col] >= 0:
                 total += 1
          else:
                 inval += 1

   print("%s ACC t=%s %2.2f%%" % (args.test, t, (match/total*100)))
