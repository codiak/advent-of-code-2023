import re

from utils import fetchInput

page = fetchInput("https://adventofcode.com/2023/day/12/input")
text_data = page.text

example = r"""
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
text_data = example

lines = text_data.strip().split('\n')

records = []
arr_counts = []

unfolded_records = []
unfolded_counts = []

for line in lines:
    halves = line.split(" ")
    condition = halves[0]
    # list(filter(None, halves[0].split(".")))
    pattern = [int(c) for c in halves[1].split(",")]
    records.append((condition, pattern))
    # Part 2: Unfold
    unf_c = "?".join([condition]*5)
    unf_p = pattern*5
    unfolded_records.append((unf_c, unf_p))


def arrangementsForPart(part: str, num: int, strict_after: bool = False):
    # Match group of ?#s without # on either side
    # (?<!#)[#?]{3}(?!#)
    # Allow overlapping matches:
    # (?=((?<!#)[#?]{3}(?!#)))
    COUNT_RE = re.compile(f"(?=((?<!#)[#?]{{{num}}}(?!#)))")
    res = COUNT_RE.finditer(part)
    indices = []
    for match in res:
        # check for invalidating #
        a = match.start()
        b = a + num + 1
        outer = part[:a]
        if strict_after:
            outer += part[b:]
        if "#" not in outer:
            indices.append(a)
    return indices


part_cache = {}


def checkAllParts(condition: str, pattern: list):
    count = 0
    n = pattern.pop(0)
    strict_after = len(pattern) == 0
    part_key = f"{condition}{pattern}"
    # use cache
    ci = 0
    if part_key in part_cache and not strict_after:
        return part_cache[part_key]
    else:
        ci =  arrangementsForPart(condition, n, strict_after)
    if len(ci) == 0 and "#" in condition:
        # nothing to match remaining #
        return 0
    if len(pattern) == 0:
        # arrangementsForPart already checks for invalidating #
        return len(ci)
    else:
        for i in ci:
            # check remaining substring for next pattern
            cutoff = i + n + 1
            sub = condition[cutoff:]
            foundc = checkAllParts(sub, pattern.copy())
            if foundc > 0:
                # valid path
                count += foundc
    if not strict_after:
        part_cache[part_key] = count
    return count


for r in records:
    count = checkAllParts(r[0], r[1])
    arr_counts.append(count)

print(f"🎁 Part 1, sum: {sum(arr_counts)}")

for i, ur in enumerate(unfolded_records):
    print(f"Part 2 progress: {i+1}/{len(unfolded_records)}")
    count = checkAllParts(ur[0], ur[1])
    unfolded_counts.append(count)

print(f"🎁 Part 2, sum: {sum(unfolded_counts)}")
