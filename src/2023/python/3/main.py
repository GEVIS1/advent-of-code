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
    part_numbers = find_part_number_indices(schematic)
    symbols = find_symbol_indices(schematic)
    valid_part_numbers = []

    print(symbols)

    for part_number, part_number_indices in part_numbers:
        part_valid = False
        for part_row, part_col in part_number_indices:
            if part_valid:
                break
            for adj_row in range(-1,2):
                for adj_col in range(-1,2):
                    row = part_row - adj_row
                    col = part_col - adj_col

                    if (row, col) in symbols:
                        part_valid = True
                        valid_part_numbers.append(part_number)


    return valid_part_numbers

def find_symbol_indices(schematic: list[str]) -> list[tuple[int, int]]:
    indices = []

    for row, row_string in enumerate(schematic):
        for col, char in enumerate(row_string):
            if is_symbol(char):
                indices.append((row, col))
    
    return indices

def is_symbol(char: str) -> bool:
    return re.match(r'^[^.0-9]$', char)

def find_part_number_indices(schematic: list[str]) -> dict[tuple[int,int], int]:
    part_numbers = []
    current_number = ''
    current_number_indices = []
    
    for row, row_string in enumerate(schematic):
        for col, char in enumerate(row_string):
            if char.isdigit():
                current_number += char
                current_number_indices.append((row, col))
            else:
                if current_number:
                    part_numbers.append((int(current_number), current_number_indices))
                    current_number = ''
                    current_number_indices = []

    return part_numbers

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
