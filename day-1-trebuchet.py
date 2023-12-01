from utils import fetchInput
import re

page = fetchInput("https://adventofcode.com/2023/day/1/input")
text_data = page.text

example = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
example2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
example3 = "75nineonethree6fourseventwonek"

lines = text_data.strip().split('\n')

RE_INT = re.compile(r'[1-9]')
values = []
num_names = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
RE_NUM_NAMES = re.compile(r'(?=(one|two|three|four|five|six|seven|eight|nine))')
MATCH_WORDS = True

for line in lines:
  intmatches = [(m.start(), int(m.group())) for m in re.finditer(RE_INT, line)]
  wordmatches = []
  if MATCH_WORDS:
    # group 1 is the word, after the non-capturing group to allow overlapping matches
    wordmatches = [(m.start(), num_names.index(m.group(1))) for m in re.finditer(RE_NUM_NAMES, line)]
  matches = intmatches + wordmatches
  # sorted uses first value of tuple by default
  sorted_matches = sorted(matches)
  parsed = int(f"{sorted_matches[0][1]}{sorted_matches[-1][1]}")
  values.append(parsed)

print(f"🎁 Sum of Values: {sum(values)}")
