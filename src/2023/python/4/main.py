import os
from functools import reduce

tests: dict[str, list[tuple[str, bool]]] = {
    'part1': [
        ('Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53', 8),
        ('Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19', 2),
        ('Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1', 2),
        ('Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83', 1),
        ('Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36', 0),
        ('Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11', 0),
    ],
    'part2': [
        ('Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53', 8),
        ('Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19', 2),
        ('Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1', 2),
        ('Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83', 1),
        ('Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36', 0),
        ('Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11', 0),
    ],
}

PART1_RESULT = 13
PART2_RESULT = 30

def calculate_score(game: str) -> tuple[bool, int]:
    game_number, winning_numbers, pulled_numbers = parse_game(game)
    score = 0

    for number in pulled_numbers:
        if number in winning_numbers:
            if score:
                score *= 2
            else:
                score = 1

    return score, game_number

def parse_game(game: str) -> tuple[int, list[int], list[int]]:
    [game_title, all_numbers] = game.split(': ')
    game_title_single_space = ' '.join(game_title.split())
    [_, game_number_raw] = game_title_single_space.split(' ')
    game_number = int(game_number_raw)
    [winning_numbers_raw, pulled_numbers_raw] = all_numbers.split(' | ')

    winning_numbers_raw = winning_numbers_raw.replace('  ', ' ')
    pulled_numbers_raw = pulled_numbers_raw.replace('  ', ' ')

    winning_numbers = []
    for number in winning_numbers_raw.split(' '):
        if number:
            winning_numbers.append(int(number))

    pulled_numbers = []
    for number in pulled_numbers_raw.split(' '):
        if number:
            pulled_numbers.append(int(number))

    return game_number, winning_numbers, pulled_numbers

def winning_numbers_from_score(score: int) -> int:
    winning_numbers = 0

    # Find winning numbers by reducing the score by two to find the power
    # since one power is one winning number
    while score > 0:
        score //= 2
        winning_numbers += 1

    return winning_numbers

if __name__ == "__main__":
    # Part 1 tests
    total_result = 0

    for game, output in tests['part1']:
        result, _ = calculate_score(game)
        assert result == output, f"Expected output ({output}), but got result ({result})."
        total_result += result

    assert total_result == PART1_RESULT, \
        f"Expected result of ({PART1_RESULT}), but got result ({total_result})"

    # Load input
    with open(os.path.dirname(__file__) + '/input.txt', encoding='utf-8') as f:
        puzzle_input = f.read()

    # Part 1 solution
    part1_solution = 0

    for line in puzzle_input.split('\n'):
        score, _ = calculate_score(line)
        part1_solution += score

    print(f'Found solution for part 1: {part1_solution}')

    # Part 2 tests
    total_result = 0
    stack = []

    for game, _ in reversed(tests['part2']):
        stack.append(game)

    total_result += len(stack)
    
    while stack:
        game = stack.pop()
        score, game_number = calculate_score(game)
        winning_numbers = winning_numbers_from_score(score)

        if winning_numbers:
            for new_game, _ in tests['part2'][game_number: (game_number + winning_numbers) % len(tests['part2'])]:
                stack.append(new_game)
                total_result += 1

    assert total_result == PART2_RESULT, \
        f"Expected result of ({PART2_RESULT}), but got result ({total_result})"
    
    # Part 2 solution
    puzzle_input_list = puzzle_input.split('\n')
    part2_solution = 0
    stack = []

    for game in reversed(puzzle_input_list):
        stack.append(game)

    part2_solution += len(stack)

    while stack:
        game = stack.pop()
        score, game_number = calculate_score(game)
        winning_numbers = winning_numbers_from_score(score)

        if winning_numbers:
            for new_game in puzzle_input_list \
                [game_number: (game_number + winning_numbers) % len(puzzle_input_list)] \
                :
                stack.append(new_game)
                part2_solution += 1

    print(f'Found solution for part 2: {part2_solution}')
