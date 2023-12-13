import re
import numpy as np

from itertools import combinations
from utils import fetchInput

page = fetchInput("https://adventofcode.com/2023/day/13/input")
text_data = page.text

example = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""
text_data = example

lines = text_data.strip().split('\n')
patterns: list = [[]]

# build reference arrays
p_i = 0
y = 0
for line in lines:
    # test if line is whitespace/newline/empty
    if re.match(r'^\s*$', line):
        y = 0
        patterns[p_i] = np.array(patterns[p_i])
        p_i += 1
        patterns.append([])
        continue
    else:
        patterns[p_i].append([])
        for x, char in enumerate(line):
            # populuate numpy array with 0s and 1s where #=1 and .=0
            # print(f" {x}, {y}: {p_i}")
            # print(patterns)
            if char == '#':
                patterns[p_i][y].append(1)
            else:
                patterns[p_i][y].append(0)
    y += 1

# convert last pattern to numpy array
patterns[len(patterns)-1] = np.array(patterns[len(patterns)-1])

row_reflections = []
col_reflections = []

for p in patterns:
    for r in range(1, p.shape[0]):
        d = min((p.shape[0] - r, r))
        r0 = r - d
        r1 = r + d
        if np.all(p[r0:r, :] == np.flip(p[r:r1, :], axis=0)):
            row_reflections.append(r)
    for c in range(1, p.shape[1]):
        d = min((p.shape[1] - c, c))
        c0 = c - d
        c1 = c + d
        if np.all(p[:, c0:c] == np.flip(p[:, c:c1], axis=1)):
            col_reflections.append(c)

summary = (100*sum(row_reflections)) + sum(col_reflections)

print(f"🎁 Part 1, summary: {summary}")
