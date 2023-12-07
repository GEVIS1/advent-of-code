import os
import re

Indice = tuple[int, int]

tests: dict[str, list[tuple[list[str], list[Indice]]]] = {
    'part1': [
        ([
            '467..114..',
            '...*......',
            '..35..633.',
            '......#...',
            '617*......',
            '.....+.58.',
            '..592.....',
            '......755.',
            '...$.*....',
            '.664.598..',
            ],
            4361)
    ],
    'part2': ['None']
}

def find_valid_schematic_parts(schematic: list[str]) -> int:
    symbols = find_symbol_indices(schematic)
    part_numbers = []

    part_number = ''
    for row, line in enumerate(schematic):
        lines = [
            schematic[row - 1] if row > 0 else '.' * len(line),
            schematic[row],
            schematic[row + 1] if row < len(schematic) - 1 else '.' * len(line)
        ]
        for col, char in enumerate(line):

            # We found the end of a number
            if not char.isdigit():
                if part_number and adjacent_to_symbol(part_number, col - len(part_number), lines):
                    part_numbers.append(int(part_number))
                part_number = ''
            # We are at the end of a line (I.E. the end of the current number)
            elif col == len(line) - 1:
                part_number += char
                if part_number and adjacent_to_symbol(part_number, col, lines):
                    part_numbers.append(int(part_number))
                part_number = ''
            else:
                part_number += char
    
    return part_numbers

def find_symbol_indices(schematic: list[str]) -> list[tuple[int, int]]:
    indices = []

    for row, row_string in enumerate(schematic):
        for col, char in enumerate(row_string):
            if is_symbol(char):
                indices.append((row, col))
    
    return indices

def is_symbol(char: str) -> bool:
    return re.match(r'^[^.0-9]$', char)

def adjacent_to_symbol(part_number: str, start_col: int, lines: list[str]) -> bool:
    part_number_row = 1

    for current_char in range(start_col, start_col + (len(part_number))):
        for row in range(-1, 2):
            for col in range(-1, 2):
                if -1 < part_number_row + row < len(lines[0]) \
                and -1 < current_char + col < len(lines[0]) \
                and is_symbol(lines[part_number_row + row][current_char + col]):
                    return True
    return False

if __name__ == "__main__":
    # Part 1 tests
    for test, output in tests['part1']:
        part_numbers = find_valid_schematic_parts(test)
        result = sum(part_numbers)

        assert result == output, \
            f"Expected result of ({output}), but got result ({result})"


    # Load input
    with open(os.path.dirname(__file__) + '/input.txt', encoding='utf-8') as f:
        puzzle_input = f.read()

    # Part 1 solution
    schematic_lines = puzzle_input.split('\n')
    # len_schematic = len(schematic_lines)
    # schematic_lines = schematic_lines[len_schematic - 3:len_schematic]
    valid_parts = find_valid_schematic_parts(schematic_lines)
    # for line in schematic_lines:
        # print(line)
    print(valid_parts)
    part1_solution = sum(valid_parts)


    print(f'Found solution for part 1: {part1_solution}')

    # # Part 2 tests
    # total_result = 0
    # first_func = [is_number, is_string_number]
    # last_func = [is_number, is_string_number]

    # for test, output in tests['part2']:
    #     first, last = find_first_and_last(first_func, last_func, test)

    #     first_number, last_number = indices_to_string(first, last, test)

    #     result = int(first_number + last_number)
    #     assert result == output, f"Expected output ({output}), but got result ({result})."
    #     total_result += result

    # assert total_result == PART2_RESULT, \
    #     f"Expected result of ({PART2_RESULT}), but got result ({total_result})"

    # # Part 2 solution
    # part2_solution = 0

    # for line in puzzle_input.split('\n'):
    #     first_index, last_index = find_first_and_last(first_func, last_func, line)
    #     first_number, last_number = indices_to_string(first_index, last_index, line)
    #     part2_solution += int(first_number + last_number)

    # print(f'Found solution for part 2: {part2_solution}')
