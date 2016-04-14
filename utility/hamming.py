#!/usr/bin/python3
import sys
import base64

def hamming_distance(x, y):
    return sum(bin(i^j).count("1") for i,j in zip(x,y))

hashes = [ bytearray(base64.b16decode(line.strip().upper())) for line in sys.std
in ]

print(hamming_distance(hashes[0], hashes[1]));

