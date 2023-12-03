import re

from utils import fetchInput

page = fetchInput("https://adventofcode.com/2023/day/3/input")
text_data = page.text

example = """........10
467..114.=
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
    # Handle end of line
    if curr_num != "":
        part_numbers.append([int(curr_num), x1, x2, y])

for part in part_numbers:
    for coord in symbol_coords:
        isNeighborRow = abs(part[3] - coord[1]) == 1
        isInXRange = (part[1] - 1) <= coord[0] <= (part[2] + 1)
        if isNeighborRow and isInXRange:
            # print("is above or below")
            real_parts.append(part[0])
            break
        elif isInXRange and part[3] == coord[1]:
            # print("is left or right")
            real_parts.append(part[0])
            break

print(f"🎁 Sum of Parts: {sum(real_parts)}")
