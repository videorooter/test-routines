#!/usr/bin/python3
import sys
import base64
import math
import itertools
import io
import argparse

def hamming_distance(x, y):
    return sum(bin(i^j).count("1") for i,j in zip(x,y))

def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element

parser = argparse.ArgumentParser(description='Cross compare fingerprints')
parser.add_argument('--max', default=50, type=int,
                   help='maximum hamming distance')
parser.add_argument('--step', default=5, type=int,
                   help='hamming distance step')
parser.add_argument('--pairs', type=argparse.FileType('w'),
                   help='output list of matching pairs')

args = parser.parse_args()


sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

data = sys.stdin.readlines()
hashes = []
filenames = {}

for d in data:
    d = d.strip()
    h, d = d.split(' ', 1)
    b = h.strip().upper()
    hashes.append(b)
    filenames[b] = [ d.strip(), bytearray(base64.b16decode(h.strip().upper())) ]

lhashes = list(set(hashes))
lhashes.sort()
hashes_a = list(itertools.combinations(lhashes, 2))

matches = {}
for i in range(0, args.max+1, args.step):
# for i in [30]:
  matches[i] = {}
count = 0
pwrite = 0
for pair in hashes_a:
    count += 1
    pdone = math.trunc(count/len(hashes_a)*100)
    if pdone != pwrite:
       print("%d done (%d%%)" % (count, count/len(hashes_a)*100), file=sys.stderr)
       pwrite = pdone
    d = hamming_distance(filenames[pair[0]][1], filenames[pair[1]][1])
    for i in matches.keys():
       if ((d <= i) and (filenames[pair[0]][0] != filenames[pair[1]][0])):
          if (args.pairs):
             print("<a href=\"%s\">A</a> - <a href=\"%s\">B</a><p />" % (filenames[pair[0]][0], filenames[pair[1]][0]), file=args.pairs)
          matches[i][filenames[pair[0]][0]] = 1
          matches[i][filenames[pair[1]][0]] = 1

print("\n * Cross compare for false positives (%d pairs, OpenImages+WM set)\n" % len(hashes_a))

for i in sorted(matches.keys()):
  print("t=%d   Matches: %d (%2.2f%%)" % (i, len(matches[i]), len(matches[i])/len(lhashes)*100))

