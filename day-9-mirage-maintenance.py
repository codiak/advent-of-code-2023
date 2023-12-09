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
extrapolated = []

for line in lines:
    seq = list(map(int, line.split()))
    seqs = [seq]
    while all(n == 0 for n in seqs[-1]) == False:
        sq = seqs[-1]
        next_seq = []
        for i in range(1, len(sq)):
            next_seq.append(sq[i] - sq[i-1])
        seqs.append(next_seq)
    # Extrapolate!
    seqs.reverse()
    for i, sq in enumerate(seqs):
        if i == 0:
            sq.append(0)
        if i+1 == len(seqs):
            extrapolated.append(sq[-1])
            break
        last = sq[-1]
        next_sq = seqs[i+1]
        next_last = next_sq[-1]
        next_sq.append(next_last + last)

print(f"🎁 Part 1, sum: {sum(extrapolated)}")
