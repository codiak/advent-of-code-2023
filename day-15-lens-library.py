import math
import re

from utils import fetchInput, loadInputFile

# page = fetchInput("https://adventofcode.com/2023/day/15/input")
# text_data = page.text
text_data = loadInputFile("day-15.txt")

example = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""

# text_data = example

lines = text_data.strip().split(',')
values = []

def hashAlgo(chars: str):
    val = 0
    for c in chars:
        val += ord(c)
        val *= 17
        val %= 256
    return val


for line in lines:
    val = hashAlgo(line)
    values.append(val)

print(f"🎁 Part 1, sum: {sum(values)}")

# Establish 256 boxes as a list
boxes = [[] for _ in range(256)]

for line in lines:
    label = "".join(re.findall(r'[a-zA-Z]', line))
    box = hashAlgo(label)
    f_len = int(line[-1]) if line[-1].isdigit() else 0
    is_remove = "-" in line
    if is_remove:
        for i, lens in enumerate(boxes[box]):
            if lens[0] == label:
                boxes[box].pop(i)
                break
    else:
        label_exists = False
        for i, lens in enumerate(boxes[box]):
            if lens[0] == label:
                label_exists = True
                boxes[box][i] = (label, f_len)
                break
        if not label_exists:
            boxes[box].append((label, f_len))


lens_power = 0

for i, box in enumerate(boxes):
    for j, lens in enumerate(box):
        pwr = (i+1) * (j+1) * lens[1]
        lens_power += pwr

# 244981
print(f"🎁 Part 2, power: {lens_power}")
