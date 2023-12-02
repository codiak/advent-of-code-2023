import math

from utils import fetchInput

page = fetchInput("https://adventofcode.com/2023/day/2/input")
text_data = page.text

example = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""
# text_data = example

lines = text_data.strip().split('\n')

avail_cubes = { "red": 12, "green": 13, "blue": 14 }
possible_games = []
game_mins = []
game_powers = []


for i, line in enumerate(lines):
    game = line.split(': ')
    game_name = game[0]
    game_data = game[1].split('; ')
    game_min = {}
    game_possible = True
    for set in game_data:
        set_data = set.strip().split(', ')
        for item in set_data:
            cube = item.split(' ')
            count = int(cube[0])
            color = cube[1]
            # Check if we have enough cubes
            if avail_cubes[cube[1]] < int(cube[0]):
                game_possible = False
            # Check for cube requirements
            if color not in game_min or count > game_min[color]:
                game_min[color] = count
    if game_possible:
        possible_games.append(i+1)
    game_mins.append(game_min)
    game_powers.append(math.prod(list(game_min.values())))

print(f"🎁 Sum of Game IDs: {sum(possible_games)}")
print(f"🎁 Sum of Game Powers: {sum(game_powers)}")
