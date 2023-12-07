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
ranks = card_rank

def evaluateHands(lines, j_is_joker=False):
    hands = []
    for i, line in enumerate(lines):
        parts = line.split(" ")
        cards = re.findall(RE_CARDS, parts[0])
        hand = {}
        jokers = 0
        for c in cards:
            if c == "J" and j_is_joker:
                jokers += 1
            elif c in hand:
                hand[c] += 1
            else:
                hand[c] = 1
        """
        Strengths:
        7. 5 of a kind
        6. 4 of a kind
        5. full house (3 of a kind + a pair)
        4. 3 of a kind
        3. 2 pair
        2. 1 pair
        1. high card (all unique)
        """
        strength = 1
        if jokers == 5:
            hand["J"] = 5
        else:
            most_of = max(hand, key=hand.get)
            if jokers > 0:
                hand[most_of] += jokers
        if 5 in hand.values():
            strength = 7
        elif 4 in hand.values():
            strength = 6
        elif 3 in hand.values():
            if 2 in hand.values():
                strength = 5
            else:
                strength = 4
        elif 2 in hand.values():
            if len(hand) == 3:
                strength = 3
            else:
                strength = 2
        elif jokers == 1:
            strength = 2
        bid = int(parts[1])
        hand["strength"] = strength
        hand["bid"] = bid
        hand["cards"] = cards
        hands.append(hand)
    return hands


def compareHands(a, b):
    if a["strength"] == b["strength"]:
        for i, ac in enumerate(a["cards"]):
            bc = b["cards"][i]
            if ranks.index(ac) == ranks.index(bc):
                continue
            else:
                if ranks.index(ac) > ranks.index(bc):
                    return 1
                else:
                    return -1
    else:
        if a["strength"] > b["strength"]:
            return 1
        else:
            return -1

# Part 1
hands_1 = evaluateHands(lines, False)
ranked_hands = sorted(hands_1, key=functools.cmp_to_key(compareHands))
winnings = 0
for i, hand in enumerate(ranked_hands):
    winnings += (i+1)*hand["bid"]

print(f"🎁 Part 1, winnings: {winnings}")

# Part 2
hands_2 = evaluateHands(lines, True)
ranks = card_rank_2
ranked_hands = sorted(hands_2, key=functools.cmp_to_key(compareHands))
winnings = 0
for i, hand in enumerate(ranked_hands):
    winnings += (i+1)*hand["bid"]

print(f"🎁 Part 2, winnings: {winnings}")
