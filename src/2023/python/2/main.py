import os
from functools import reduce

tests: dict[str, list[tuple[str, bool]]] = {
    'part1': [
        ('Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green', True),
        ('Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue', True),
        ('Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red', False),
        ('Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red', False),
        ('Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green', True),
    ],
    'part2': [
        ('Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green', 48),
        ('Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue', 12),
        ('Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red', 1560),
        ('Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red', 630),
        ('Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green', 36),
    ],
}

PART1_RESULT = 8
PART2_RESULT = 2286

DICE: dict[str, int] = {
    'red': 12,
    'green': 13, 
    'blue': 14,
}

def validate_game(game: str) -> tuple[bool, int]:
    valid = True
    game_number, pulled_dice = parse_game(game)

    for sub_dice in pulled_dice:
        for dice_colour, dice_count in sub_dice.items():
            if dice_count > DICE[dice_colour]:
                valid = False

    assert int(game_number), f'Could not parse game_number ({game_number})'

    return valid, game_number

def parse_game(game: str) -> tuple[int, list[dict[str, int]]]:
    [game_title, pulled_dice_raw] = game.split(': ')
    [_, game_number_raw] = game_title.split(' ')
    game_number = int(game_number_raw)
    pulled_dice = parse_pulled_dice(pulled_dice_raw)

    return game_number, pulled_dice

def parse_pulled_dice(raw_dice: str) -> list[dict[str, int]]:
    result = []
    for sub_dice in raw_dice.split('; '):
        pulled_dice = {}
        for dice in sub_dice.split(', '):
            [number_raw, colour] = dice.split(' ')
            number = int(number_raw)
            pulled_dice[colour] = number

        result.append(pulled_dice)

    return result

def calculate_game_power(game: str) -> int:
    [_, pulled_dice] = parse_game(game)
    max_of_colour: dict[str, int] = {}

    for pull in pulled_dice:
        for color, number in pull.items():
            if not color in max_of_colour:
                max_of_colour[color] = number
            elif number > max_of_colour[color]:
                max_of_colour[color] = number

    power = reduce(lambda acc, cur: acc * cur, max_of_colour.values())

    return power

if __name__ == "__main__":
    # Part 1 tests
    total_result = 0

    for game, output in tests['part1']:
        result, game_number = validate_game(game)
        assert result == output, f"Expected output ({output}), but got result ({result})."

        if result:
            total_result += game_number

    assert total_result == PART1_RESULT, \
        f"Expected result of ({PART1_RESULT}), but got result ({total_result})"

    # Load input
    with open(os.path.dirname(__file__) + '/input.txt', encoding='utf-8') as f:
        puzzle_input = f.read()

    # Part 1 solution
    part1_solution = 0

    for line in puzzle_input.split('\n'):
        valid, game_number = validate_game(line)
        if valid:
            part1_solution += game_number

    print(f'Found solution for part 1: {part1_solution}')

    # Part 2 tests
    total_result = 0

    for game, output in tests['part2']:
        result = calculate_game_power(game)
        assert result == output, f"Expected output ({output}), but got result ({result})."
        total_result += result

    assert total_result == PART2_RESULT, \
        f"Expected result of ({PART2_RESULT}), but got result ({total_result})"
    
    # Part 2 solution
    part2_solution = 0

    for line in puzzle_input.split('\n'):
        game_power = calculate_game_power(line)
        part2_solution += game_power

    print(f'Found solution for part 2: {part2_solution}')
