import re
import numpy as np
from numpy.typing import NDArray

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
example_2 = """
#...##.
#.#####
#.....#
...####
.#.....
####..#
.#..##.
#..####
#..####
"""
text_data = example
lines = text_data.strip().split('\n')

patterns: list = [[]]
row_reflections = []
col_reflections = []
row_reflections_2 = []
col_reflections_2 = []

# build reference arrays
p_i = 0
y = 0
for line in lines:
    if re.match(r'^\s*$', line):
        y = 0
        patterns[p_i] = np.array(patterns[p_i])
        p_i += 1
        patterns.append([])
        continue
    else:
        patterns[p_i].append([])
        for x, char in enumerate(line):
            if char == '#':
                patterns[p_i][y].append(1)
            else:
                patterns[p_i][y].append(0)
    y += 1

# convert last to numpy array
patterns[-1] = np.array(patterns[-1])


def get_reflection(p: NDArray, smudge = None) -> tuple[int, int]:
    for r in range(1, p.shape[0]):
        d = min((p.shape[0] - r, r))
        r0 = r - d
        r1 = r + d
        if smudge and (smudge[0] <= r0 or smudge[0] >= r1):
            continue
        if np.all(p[r0:r, :] == np.flip(p[r:r1, :], axis=0)):
            return (r, 0)
    for c in range(1, p.shape[1]):
        d = min((p.shape[1] - c, c))
        c0 = c - d
        c1 = c + d
        if smudge and (smudge[1] <= c0 or smudge[1] >= c1):
            continue
        if np.all(p[:, c0:c] == np.flip(p[:, c:c1], axis=1)):
            return (0, c)
    return (0,0)


def find_smudge_and_reflect(p: NDArray) -> tuple[int, int]:
    for r in range(0, p.shape[0]):
        for c in range(0, p.shape[1]):
            p_copy = np.copy(p)
            # smudge flip
            p_copy[r,c] ^= 1
            reflect = get_reflection(p_copy, (r,c))
            if reflect != (0,0):
                return reflect
    raise Exception("No smudge found")


for p in patterns:
    init_reflect = get_reflection(p)
    row_reflections.append(init_reflect[0])
    col_reflections.append(init_reflect[1])
    # Part 2
    reflect_2 = find_smudge_and_reflect(p)
    row_reflections_2.append(reflect_2[0])
    col_reflections_2.append(reflect_2[1])

summary = (100*sum(row_reflections)) + sum(col_reflections)
summary_2 = (100*sum(row_reflections_2)) + sum(col_reflections_2)

print(f"🎁 Part 1, summary: {summary}")
print(f"🎁 Part 2, summary: {summary_2}")
