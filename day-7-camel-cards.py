import re
import functools

from utils import fetchInput

page = fetchInput("https://adventofcode.com/2023/day/7/input")
text_data = page.text

example = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
# text_data = example

lines = text_data.strip().split('\n')

RE_INT = re.compile(r'[0-9]')
RE_CARDS = re.compile(r'[2-9AKQJT]')
card_rank = "23456789TJQKA"
card_rank_2 = "J23456789TQKA"

# 7. 5 of a kind
# 6. 4 of a kind
# 5. full house
# 4. 3 of a kind
# 3. 2 pair
# 2. 1 pair
# 1. high card (all unique)
hands = []

# Evaluate hands
for i, line in enumerate(lines):
    parts = line.split(" ")
    cards = re.findall(RE_CARDS, parts[0])
    hand = {}
    for c in cards:
        if c in hand:
            hand[c] += 1
        else:
            hand[c] = 1
    strength = 1
    # Part 2
    jokers = hand.get('J', 0)
    if len(hand) == 1:
        strength = 7
    elif len(hand) == 2:
        if 4 in hand.values():
            strength = 6
        else:
            strength = 5
    elif len(hand) == 3:
        if 3 in hand.values():
            strength = 4
        else:
            # 2 pair
            strength = 3
    elif len(hand) == 4:
        strength = 2
    strength += jokers
    bid = int(parts[1])
    hand["strength"] = strength
    hand["bid"] = bid
    hand["cards"] = cards
    hand["jokers"] = jokers
    hands.append(hand)

# Rank hands
def compareHands(a, b):
    if a["strength"] == b["strength"]:
        for i, ac in enumerate(a["cards"]):
            bc = b["cards"][i]
            if card_rank_2.index(ac) == card_rank_2.index(bc):
                continue
            else:
                if card_rank_2.index(ac) > card_rank_2.index(bc):
                    return 1
                else:
                    return -1
    else:
        if a["strength"] > b["strength"]:
            return 1
        else:
            return -1

ranked_hands = sorted(hands, key=functools.cmp_to_key(compareHands))

print(ranked_hands)
total_winnings = 0
for i, hand in enumerate(ranked_hands):
    total_winnings += (i+1)*hand["bid"]

# 247084283 too low
print(f"🎁 Part 1, winnings: {total_winnings}")
