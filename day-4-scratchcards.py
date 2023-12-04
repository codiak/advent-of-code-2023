import re

from utils import fetchInput

page = fetchInput("https://adventofcode.com/2023/day/4/input")
text_data = page.text

example = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
# text_data = example

lines = text_data.strip().split('\n')

scores = []
copy_counts = [1]*len(lines)

for i, line in enumerate(lines):
    str_list = re.split(r':|\|', line)
    winning = re.split(r'\s+', str_list[1].strip())
    numbers = re.split(r'\s+', str_list[2].strip())
    count = 0
    for x in numbers:
        if x in winning:
            count += 1
    if count > 0:
        scores.append(2**(count - 1))
    # Part 2
    win_x = copy_counts[i]
    for c in range(i+1, i+count+1):
        if c >= len(copy_counts):
            copy_counts.append(win_x)
        else:
            copy_counts[c] += win_x

print(f"🎁 Total score: {sum(scores)}")
print(f"🎁 Total copies: {sum(copy_counts)}")
