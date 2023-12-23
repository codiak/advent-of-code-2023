import math
import re

from utils import loadInputFile

text_data = loadInputFile("day-22.txt")

example = """
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""

text_data = example

lines = text_data.strip().split('\n')
occupied_list = []

class Brick:
    def __init__(self, a, b, name):
        self.a = a
        self.b = b
        self.name = name

    def __str__(self):
        return f"Brick {self.name}"


def int_to_alphabetic_label(n):
    label = ''
    while n >= 0:
        n, remainder = divmod(n, 26)
        label = chr(65 + remainder) + label
        n -= 1
    return label


bricks = []

for i, line in enumerate(lines):
    print(line)
    a, b = line.split('~')
    x, y, z = map(int, a.split(','))
    xb, yb, zb = map(int, b.split(','))
    name = int_to_alphabetic_label(i)
    bricks.append(Brick((x,y,z), (xb, yb, zb), name))
    occupied_list.append((x,y,z))
    occupied_list.append((xb,yb,zb))

# sort list ascending
occupied_lists = sorted(occupied_list, key=lambda x: (x[2], x[0], x[1]))

print(list(map(str, bricks)))
print(occupied_lists)

# Work way up from z=1, and settle each brick
