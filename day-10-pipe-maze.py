import re
import functools
import math

from utils import fetchInput

page = fetchInput("https://adventofcode.com/2023/day/10/input")
text_data = page.text

example = """
.....
.S-7.
.|.|.
.L-J.
.....
"""
example_2 = """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""
# text_data = example_2

lines = text_data.strip().split('\n')
dir_map = {
    "|": (1,0,1,0),
    "-": (0,1,0,1),
    "L": (1,1,0,0),
    "J": (1,0,0,1),
    "7": (0,0,1,1),
    "F": (0,1,1,0),
    "S": (1,1,1,1)
}
start = (0,0)
pipes = []
farthest = 0
y_len = len(lines)
x_len = len(lines[0])

class Pipe:
    def __init__(self, x, y, dirs):
        self.x = x
        self.y = y
        self.dirs = dirs
        self.visitedFrom = [0,0,0,0]
        self.distance = 0

# Build Network
for y, line in enumerate(lines):
    y_list = []
    for x, c in enumerate(line):
        # print(f"Adding: {c} at {x}, {y}")
        if c == '.':
            y_list.append(None)
        else:
            y_list.append(Pipe(x, y, dir_map[c]))
            if c == 'S':
                start = (x, y)
    pipes.append(y_list)

# Navigate network using FIFO queue
pipe_queue = [(pipes[start[1]][start[0]], [])]
while len(pipe_queue) > 0:
    val = pipe_queue.pop(0)
    curr = val[0]
    path = val[1].copy()
    if curr is None or (curr.x, curr.y) in path:
        continue
    # print(f"Checking: {curr.x}, {curr.y}")
    # curr.visited = True
    new_dist = len(path)
    if curr.distance == 0 or new_dist < curr.distance:
        curr.distance = new_dist
    path.append((curr.x, curr.y))
    if curr.distance > farthest:
        farthest = curr.distance
    # if curr.distance == 9:
    #     print(path)
    # Up
    if curr.dirs[0] == 1 and curr.y > 0:
        up = pipes[curr.y-1][curr.x]
        # if up != None and up.visitedFrom[2] == 0:
        if up != None and up.dirs[2] == 1:
                pipes[curr.y-1][curr.x].visitedFrom[2] = 1
                pipe_queue.append((pipes[curr.y-1][curr.x], path))
    # Right
    if curr.dirs[1] == 1 and curr.x < x_len-1:
        right = pipes[curr.y][curr.x+1]
        # if right != None and right.visitedFrom[3] == 0:
        if right != None and right.dirs[3] == 1:
                pipes[curr.y][curr.x+1].visitedFrom[3] = 1
                pipe_queue.append((pipes[curr.y][curr.x+1], path))
    # Down
    if curr.dirs[2] == 1 and curr.y < y_len-1:
        down = pipes[curr.y+1][curr.x]
        # if down != None and down.visitedFrom[0] == 0:
        if down != None and down.dirs[0] == 1:
                pipes[curr.y+1][curr.x].visitedFrom[0] = 1
                pipe_queue.append((pipes[curr.y+1][curr.x], path))
    # Left
    if curr.dirs[3] == 1 and curr.x > 0:
        left = pipes[curr.y][curr.x-1]
        # if left != None and left.visitedFrom[1] == 0:
        if left != None and left.dirs[1] == 1:
                pipes[curr.y][curr.x-1].visitedFrom[1] = 1
                pipe_queue.append((pipes[curr.y][curr.x-1], path))

print(f"🎁 Part 1, farthest: {farthest}")

# Debug map
# for y_row in pipes:
#     for x in y_row:
#         if x is None:
#             print(" ", end="")
#         elif x.distance == 0:
#             print(" ", end="")
#         else:
#             print(x.distance, end="")
#     print("")
