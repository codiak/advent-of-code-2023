import numpy as np
import time
from numpy.typing import NDArray

from utils import loadInputFile

text_data = loadInputFile("day-14.txt")

example = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
text_data = example

lines = text_data.strip().split('\n')
rock_map: list = []
rock_arr: NDArray[np.int64] = np.array([])
chars = { ".": 0, "O": 1,  "#": 2 }
timing = { 'N': 0, 'S': 0, 'E': 0, 'W': 0}

for y, line in enumerate(lines):
    # rock_map.append([])
    l = []
    for x, c in enumerate(line):
        l.append(chars[c])
    rock_map.append(np.array(l))

rock_arr = np.array(rock_map)

def tilt_up(col):
    prev = None
    moved = False
    for i, space in enumerate(col):
        if space == 1 and prev == 0:
            moved = True
            col[i] = 0
            col[i-1] = 1
        prev = space
    # repeat until no more movement
    if moved:
        col = tilt_up(col)
    return col


def get_load(arr):
    load = 0
    cols = arr.T
    for col in cols:
        for i, space in enumerate(col):
            if space == 1:
                load += len(col) - i;
    return load


def tilt(arr, direction = 'N'):
    start = time.time()
    if direction == 'N':
        cols = arr.T
    elif direction == 'S':
        # cols = np.flip(arr.T, 0)
        cols = np.flip(arr, 0).T
    elif direction == 'E':
        cols = np.flip(arr, 1)
    else:
        cols = arr
    for c in cols:
       c = tilt_up(c)
    # flip array back
    if direction == 'N':
        arr = cols.T
        # cols[::-1,::-1].T
    elif direction == 'S':
        arr = np.flip(cols.T, 0)
    elif direction == 'E':
        arr = np.flip(cols, 1)
        # arr = cols
    else:
        arr = cols
    timing[direction] += time.time() - start
    return arr

def cycle(arr, times = 1):
    for i in range(times):
        arr = tilt(arr, 'N')
        arr = tilt(arr, 'W')
        arr = tilt(arr, 'S')
        arr = tilt(arr, 'E')
        if (rock_arr == arr).all():
            print(f"Cycle {i+1}, pattern repeats")
    return arr

a = tilt(np.copy(rock_arr))
north_load = get_load(a)

print(f"🎁 Part 1, sum: {north_load}")


a2 = cycle(np.copy(rock_arr), 1000)
load_2 = get_load(a2)

print(f"🎁 Part 2, north support: {np.sum(a2)}")
print(timing)
# for row in a2:
#     print(row)
