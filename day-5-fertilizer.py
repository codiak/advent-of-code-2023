import re

from utils import fetchInput

page = fetchInput("https://adventofcode.com/2023/day/5/input")
text_data = page.text

example = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
# text_data = example

text_sections = text_data.strip().split('\n\n')
seed_str = text_sections.pop(0)
seed_str = seed_str.replace("seeds:", "").strip()

maps = {}
current_map = "seed"
values = [int(s) for s in seed_str.split()]

# Part 2
value_ranges = []
current_range_map = "seed"
for i in range(0, len(values), 2):
    x = values[i]
    value_ranges.append((x, x+values[i+1]))


class AlmanacMap:
    def __init__(self, source, destination):
        self.source = source
        self.destinatiton = destination
        self.ranges = []

    def map(self, value):
        for r in self.ranges:
            if value >= r[0] and value <= r[1]:
                return value + r[2]
        return value

    def map_range(self, start, end):
        start_mapped = start
        end_mapped = end
        unmapped = None
        for r in self.ranges:
            start_in_range = start >= r[0] and start <= r[1]
            end_in_range = end >= r[0] and end <= r[1]
            if start_in_range and end_in_range:
                start_mapped = start + r[2]
                end_mapped = end + r[2]
                break
            elif start_in_range:
                start_mapped = (start + r[2], r[1] + r[2])
                unmapped = (r[1] + 1, end)
                break
            elif end_in_range:
                end_mapped = (r[0] + r[2], end + r[2])
                unmapped = (start, r[0] - 1)
                break
        return (start_mapped, end_mapped, unmapped)

    def add_range(self, values):
        self.ranges.append(values)
        self.ranges.sort()


# Build Maps
for i, map_str in enumerate(text_sections):
    map_lines = map_str.strip().split('\n')
    map_def = map_lines.pop(0).replace(" map:", "")
    map_labels = map_def.split("-to-")
    map = AlmanacMap(map_labels[0], map_labels[1])
    for i, line in enumerate(map_lines):
        num_str = line.split()
        nums = [int(n) for n in num_str]
        x = nums[2] - 1
        diff = nums[0] - nums[1]
        map.add_range((nums[1], nums[1]+x, diff))
    map.ranges.sort()
    maps[map.source] = map

# Part 1
while current_map != "location":
    for i, val in enumerate(values):
        values[i] = maps[current_map].map(val)
    current_map = maps[current_map].destinatiton

print(f"🎁 Part 1, minimum: {min(values)}")

# Part 2
while current_range_map != "location":
    for i, val_tup in enumerate(value_ranges):
        mapped_ranges = maps[current_range_map].map_range(val_tup[0], val_tup[1])
        start_split = isinstance(mapped_ranges[0], tuple)
        end_split = isinstance(mapped_ranges[1], tuple)
        unmapped = mapped_ranges[2] is not None
        if start_split:
            value_ranges[i] = mapped_ranges[0]
        elif end_split:
            value_ranges[i] = mapped_ranges[1]
        else:
            value_ranges[i] = mapped_ranges
        # Add new range introduced by overlap/split
        if unmapped:
            value_ranges.append(mapped_ranges[2])
    current_range_map = maps[current_range_map].destinatiton
    print(f"🌱 Part 2, Mapping Progress: {current_range_map}")

print(f"🎁 Part 2, minimum range: {min(value_ranges)}")
