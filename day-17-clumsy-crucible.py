import math
import heapq
from collections import defaultdict

from utils import loadInputFile

text_data = loadInputFile("day-17.txt")

example = """
111111111111
999999999991
999999999991
999999999991
999999999991
"""
# text_data = example

lines = text_data.strip().split('\n')
start = (0, 0)
finish = (len(lines[0]) - 1, len(lines) - 1)


def find_lowest_heat_lost(lines, min_repeat=0, max_repeat=3):
    finish = (len(lines[0]) - 1, len(lines) - 1)
    # Priority queue prioritizes low heat loss paths
    queue = [(0, (0, 0), -1, 0)]  # (heat_lost, position, dir, repeat)
    heat_losses = []

    total_heat = defaultdict(lambda: math.inf)
    total_heat[(0, 0, -1, 0)] = 0

    while queue:
        heat_lost, (x, y), dir, repeat = heapq.heappop(queue)
        # debug
        # print(heat_lost, (x, y), dir, repeat)

        if (x, y) == finish and repeat >= min_repeat:
            return heat_lost

        not_allowed = { -1:4, 0:2, 1:3, 2:0, 3:1}
        for dx, dy, new_dir in [(0,-1,0), (1,0,1), (0,1,2), (-1,0,3)]:
            nx, ny = x + dx, y + dy
            new_repeat = repeat + 1 if new_dir == dir else 1
            if dir != -1:
                if repeat < min_repeat and new_dir != dir:
                    continue
            if new_repeat > max_repeat and new_dir == dir:
                continue
            if new_dir == not_allowed[dir]:
                continue
            # Check if bounded move
            if 0 <= nx <= finish[0] and 0 <= ny <= finish[1]:
                new_t = (nx, ny, new_dir, new_repeat)
                new_heat_lost = heat_lost + int(lines[ny][nx])
                if new_heat_lost < total_heat[new_t]:
                    total_heat[new_t] = new_heat_lost
                    heapq.heappush(queue, (new_heat_lost, (nx, ny), new_dir, new_repeat))
    return math.inf

lowest = find_lowest_heat_lost(lines)
print(f"🎁 Part 1, lowest heat loss: {lowest}")

lowest_2 = find_lowest_heat_lost(lines, 4, 10)
print(f"🎁 Part 2, lowest ultra heat loss: {lowest_2}")
