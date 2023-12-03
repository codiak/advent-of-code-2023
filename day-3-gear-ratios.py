import re

from utils import fetchInput

page = fetchInput("https://adventofcode.com/2023/day/3/input")
text_data = page.text

example = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""
# text_data = example

lines = text_data.strip().split('\n')

RE_INT = re.compile(r'[0-9]')

symbol_coords = []
part_numbers = []
real_parts = []
real_part_numbers = []
gears = []
gear_ratios = []

for y, line in enumerate(lines):
    curr_num = ""
    x1 = None
    x2 = None
    for x, char in enumerate(line):
        if re.match(RE_INT, char):
            if x1 is None:
                x1 = x
            x2 = x
            curr_num += char
            continue
        else:
            if curr_num != "":
                part_numbers.append([int(curr_num), x1, x2, y])
            curr_num = ""
            x1 = None
            x2 = None
            if char != ".":
                # is special character
                symbol_coords.append((x, y))
            if char == "*":
                gears.append((x, y))
    # Handle end of line
    if curr_num != "":
        part_numbers.append([int(curr_num), x1, x2, y])


def isAdjacent(a1, a2, b1):
    isNeighborRow = abs(a1[1] - b1[1]) == 1
    isInXRange = (a1[0] - 1) <= b1[0] <= (a2[0] + 1)
    isAbove = isNeighborRow and isInXRange
    isLeftOrRight = isInXRange and a1[1] == b1[1]
    if isAbove or isLeftOrRight:
        return True
    else:
        return False


for p in part_numbers:
    for coord in symbol_coords:
        if isAdjacent((p[1], p[3]), (p[2], p[3]), coord):
            real_parts.append(p)
            real_part_numbers.append(p[0])
            break

for gear in gears:
    adjacent_nums = []
    for p in real_parts:
        if isAdjacent((p[1], p[3]), (p[2], p[3]), gear):
            adjacent_nums.append(p[0])
    if len(adjacent_nums) == 2:
        ratio = adjacent_nums[0] * adjacent_nums[1]
        gear_ratios.append(ratio)


print(f"🎁 Sum of Parts: {sum(real_part_numbers)}")
print(f"🎁 Sum of Ratios: {sum(gear_ratios)}")
