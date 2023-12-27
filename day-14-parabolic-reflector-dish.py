import numpy as np
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
arr_at_cycle = []

for y, line in enumerate(lines):
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
    cols = np.rot90(arr, 1)
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
    elif direction == 'S':
        arr = np.flip(cols.T, 0)
    elif direction == 'E':
        arr = np.flip(cols, 1)
    else:
        arr = cols
    return arr


def cycle(arr, times = 1):
    s = 0
    dirs = ['N', 'W', 'S', 'E']
    cycles_skipped = False
    tilts = 4*times
    while s < tilts:
        dir = dirs[s % 4]
        arr = tilt(arr, dir)
        if not cycles_skipped and dir == 'E':
            for j, arr_hash in enumerate(arr_at_cycle):
                if arr_hash == hash(bytes(arr)):
                    step = len(arr_at_cycle)
                    print(f"Step {step} (to {j}), {dir}, pattern repeats")
                    cyc_len = step - j
                    remainder = (tilts - s) % cyc_len
                    s = tilts - remainder - 1
                    cycles_skipped = True
                    break
        arr_at_cycle.append(hash(bytes(arr)))
        s += 1
    return arr


a = tilt(np.copy(rock_arr))
north_load = get_load(a)

print(f"🎁 Part 1, sum: {north_load}")

a2 = cycle(np.copy(rock_arr), 1000000000)
load_2 = get_load(a2)

# Without cycle detection:
# .23s for 1000 cycles
# 293s for 1000000 (example)
# With:
# .003s for 1B cycles (example)
# 7.8s for 1B cycles (input)

print(f"🎁 Part 2, north support: {load_2}")
