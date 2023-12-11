import re
import functools
import math
import numpy as np
from itertools import combinations
from utils import fetchInput

page = fetchInput("https://adventofcode.com/2023/day/11/input")
text_data = page.text

example = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""
# text_data = example

lines = text_data.strip().split('\n')
galaxies = []
empty_rows = list(range(0, len(lines)))
empty_cols = list(range(0, len(lines[0])))

# build reference lists
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == '#':
            galaxies.append([x, y])
            if y in empty_rows:
                empty_rows.remove(y)
            if x in empty_cols:
                empty_cols.remove(x)

def expand_space_get_dists(galaxies, multiple=2):
    for g in galaxies:
        x_shift = 0
        y_shift = 0
        for ci, c in enumerate(empty_cols):
            if g[0] > c:
                x_shift = ((ci+1)*multiple)-(ci+1)
        for ri, r in enumerate(empty_rows):
            if g[1] > r:
                y_shift = ((ri+1)*multiple)-(ri+1)
        # shift galaxy
        g[0] = g[0] + x_shift
        g[1] = g[1] + y_shift
    distances = []
    gal_combos = combinations(galaxies, 2)

    for combo in gal_combos:
        gA = combo[0]
        gB = combo[1]
        distances.append(abs(gA[0]-gB[0]) + abs(gA[1]-gB[1]))
    return distances

distances = expand_space_get_dists(galaxies)
distances_2 = expand_space_get_dists(galaxies, multiple=1000000)

print(f"🎁 Part 1, sum of distances: {sum(distances)}")
print(f"🎁 Part 2, sum of distances: {sum(distances_2)}")
