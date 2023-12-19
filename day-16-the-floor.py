import sys

from utils import fetchInput

page = fetchInput("https://adventofcode.com/2023/day/16/input")
text_data = page.text
sys.setrecursionlimit(10000)

example = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""
text_data = example

lines = text_data.strip().split('\n')
dir_map = []
pwrd = []


def getNextDiff(char, diff):
    if char == "|" and diff[1] == 0:
        return [(0, -1), (0, 1)]
    elif char == "-" and diff[0] == 0:
        return [(-1, 0), (1, 0)]
    elif char == "\\":
        return [(diff[1], diff[0])]
    elif char == "/":
        return [(diff[1]*-1, diff[0]*-1)]
    elif char in [".", "|", "-"]:
        return [diff]
    else:
        # reached edge
        return None


def navSpace(pt, diff):
    if pt[0] < 0 or pt[1] < 0 or pt[0] >= len(lines[0]) or pt[1] >= len(lines):
        # print("reached edge")
        return
    if pt not in pwrd:
        pwrd.append(pt)
    char = lines[pt[1]][pt[0]]
    dlist = getNextDiff(char, diff)
    if dlist is None:
        print("Should not reach")
    else:
        for nd in dlist:
            new_pt = (pt[0] + nd[0], pt[1] + nd[1])
            dir_note = (new_pt, nd)
            if dir_note not in dir_map:
                dir_map.append(dir_note)
                navSpace(new_pt, nd)

# run from top left
pwrd.append((0, 0))
dir_map.append(((0, 0), (1, 0)))
navSpace((0, 0), (1, 0))

print(f"🎁 Part 1, sum: {len(pwrd)}")


# Part 2
# Brute force is a bit slow, but it works

poss_pwrd = []

def testEntry(pt, diff):
    global pwrd
    global dir_map
    global poss_pwrd
    pwrd = []
    dir_map = []
    pwrd.append(pt)
    navSpace(pt, diff)
    poss_pwrd.append(len(pwrd))

for w in range(len(lines[0])):
    # from top
    testEntry((w, 0), (0, 1))
    # from bottom
    testEntry((w, len(lines)-1), (0, -1))

for h in range(len(lines)):
    # from left
    testEntry((0, h), (1, 0))
    # from right
    testEntry((len(lines[0])-1, h), (-1, 0))

print(f"🎁 Part 2, max: {max(poss_pwrd)}")
