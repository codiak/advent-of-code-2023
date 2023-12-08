import re
import functools
import math

from utils import fetchInput

page = fetchInput("https://adventofcode.com/2023/day/8/input")
text_data = page.text

example = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""
example_2 = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""
# text_data = example_2

lines = text_data.strip().split('\n')
instructions = lines.pop(0)
lines = list(filter(None, lines))

RE_LOC = re.compile(r'[0-9A-Z]{3}')
pointer_dict = {}
starting_nodes = []

class Node:
    def __init__(self, loc, left, right):
        self.loc = loc
        self.left = left
        self.right = right


# Build Network/Tree
for line in lines:
    locs = re.findall(RE_LOC, line)
    curr = locs[0]
    l_loc = locs[1]
    r_loc = locs[2]
    if l_loc not in pointer_dict:
        pointer_dict[l_loc] = Node(l_loc, None, None)
    if r_loc not in pointer_dict:
        pointer_dict[r_loc] = Node(r_loc, None, None)
    left = pointer_dict[l_loc]
    right = pointer_dict[r_loc]
    if curr in pointer_dict:
        pointer_dict[curr].left = left
        pointer_dict[curr].right = right
    else:
        pointer_dict[curr] = Node(curr, left, right)
    if curr[2] == "A":
        starting_nodes.append(pointer_dict[curr])

# Follow instructions
def navigate_to_z(start_node):
    current_node = start_node
    n_steps = 0
    while current_node.loc[2] != "Z":
        for step in instructions:
            n_steps += 1
            if step == "L":
                current_node = current_node.left
            elif step == "R":
                current_node = current_node.right
            if current_node.loc[2] == "Z":
                break
    return n_steps

steps_1 = navigate_to_z(pointer_dict["AAA"])
print(f"🎁 Part 1, steps: {steps_1}")

# Part 2
all_steps = []
for start in starting_nodes:
    all_steps.append(navigate_to_z(start))
steps_2 = math.lcm(*all_steps)
print(f"🎁 Part 2, steps: {steps_2}")

# For posterity: Initial brute force attempt
# def multi_nav_to_z(nodes):
#     nodes_at_z = []
#     n_steps = 0
#     while len(nodes_at_z) != len(nodes):
#         nodes_at_z = []
#         step = instructions[n_steps%len(instructions)]
#         for i, node in enumerate(nodes):
#             # print(node.loc)
#             # print(step)
#             if step == "L":
#                 nodes[i] = node.left
#             elif step == "R":
#                 nodes[i] = node.right
#             if nodes[i].loc[2] == "Z":
#                 nodes_at_z.append(nodes[i].loc)
#         n_steps += 1
#     return n_steps

# # 19783 too low
# print(starting_nodes)
# steps_2 = multi_nav_to_z(starting_nodes)
