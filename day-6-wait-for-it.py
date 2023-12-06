import re
from functools import reduce
from utils import fetchInput

page = fetchInput("https://adventofcode.com/2023/day/6/input")
text_data = page.text

example = """
Time:      7  15   30
Distance:  9  40  200
"""
text_data = example

lines = text_data.strip().split('\n')
RE_INT = re.compile(r'[0-9]+')

times = re.findall(RE_INT, lines[0])
distances = re.findall(RE_INT, lines[1])
# Part 2
big_lines = list(map(lambda x: x.replace(" ", ""), lines))
big_time = re.findall(RE_INT, big_lines[0])
big_distance = re.findall(RE_INT, big_lines[1])


def get_winning_speeds(ts, ds):
    ways = []
    for i, time in enumerate(ts):
        r = int(ds[i])
        t = int(time)
        winning_speeds = []
        # (time - speed) * speed = record
        for s in range(0, t):
            if (t - s) * s > r:
                winning_speeds.append(s)
        ways.append(len(winning_speeds))
    return ways

p1_ways = get_winning_speeds(times, distances)
margin = reduce(lambda x, y: x*y, p1_ways)

print(f"🎁 Part 1, margin: {margin}")

p2_ways = get_winning_speeds(big_time, big_distance)

print(f"🎁 Part 2, ways: {p2_ways}")
