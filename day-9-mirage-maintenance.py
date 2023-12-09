import re
import functools
import math

from utils import fetchInput

page = fetchInput("https://adventofcode.com/2023/day/9/input")
text_data = page.text

example = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""
# text_data = example

lines = text_data.strip().split('\n')
extrapolated_1 = []
extrapolated_2 = []


def extrapolate(seqs, op=1):
    for i, sq in enumerate(seqs):
        if i == 0:
            sq.append(0)
        if i+1 == len(seqs):
            return sq[-1]
        next_last = seqs[i+1][-1]
        seqs[i+1].append(next_last + (op*sq[-1]))


for line in lines:
    seq = list(map(int, line.split()))
    seqs = [seq]
    while all(n == 0 for n in seqs[-1]) == False:
        next_seq = []
        for i in range(1, len(seqs[-1])):
            next_seq.append(seqs[-1][i] - seqs[-1][i-1])
        seqs.append(next_seq)
    seqs.reverse()
    extrapolated_1.append(extrapolate(seqs))
    # Part 2
    rev_seqs = [s.reverse() for s in seqs]
    extrapolated_2.append(extrapolate(seqs, -1))

print(f"🎁 Part 1, sum: {sum(extrapolated_1)}")
print(f"🎁 Part 2, sum: {sum(extrapolated_2)}")
