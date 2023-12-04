from typing import Iterable
import os

Input = str
Output = str
TestCase = tuple[Input, Output]

tests: dict[str, list[TestCase]] = {
    'part1': [
        ('1abc2', 12),
        ('pqr3stu8vwx', 38),
        ('a1b2c3d4e5f', 15),
        ('treb7uchet', 77),
    ],
    'part2': [
        ('two1nine', 29),
        ('eightwothree', 83),
        ('abcone2threexyz', 13),
        ('xtwone3four', 24),
        ('4nineeightseven2', 42),
        ('zoneight234', 14),
        ('7pqrstsixteen', 76),
    ]
}

PART1_RESULT = 142
PART2_RESULT = 281

def find_first_and_last(first: list[callable], last: list[callable], iterable: Iterable) -> tuple[int, int]:
    match iterable:
        case l if isinstance(iterable, str):
            i1 = 0
            i2 = len(l) - 1
            found = False


            while not found:
                function_index = 0
                correct_first = None
                correct_last  = None

                while correct_first is None and function_index < len(first):
                    correct_first = first[function_index](l, i1)
                    function_index += 1

                function_index = 0

                while correct_last is None and function_index < len(last):
                    correct_last  = last[function_index](l, i2)
                    function_index += 1

                if correct_first is None:
                    i1 += 1
                if correct_last is None:
                    i2 -= 1

                if correct_first is not None and correct_last is not None:
                    found = True
                elif i1 > i2 or i2 < i1:
                    raise RuntimeError(
                        "Indices converged at centre and no first and last values were found."
                        )
        case _:
            raise NotImplementedError(f"{type(iterable)} support not implemented")

    return (correct_first, correct_last)

def is_number(l: Iterable, i: int) -> int | None:
    try:
        isinstance(int(l[i]), int)
    except ValueError as _:
        return None

    return i

DECIMAL_NUMBER_STRINGS: dict[str, int] = {
    'zero': 0,
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

def is_string_number(l: Iterable, i: int) -> tuple[int, int] | None:
    for number in DECIMAL_NUMBER_STRINGS.keys():
        if number == l[i: i + len(number)]:
            return i, i + len(number)

    return None

def indices_to_string(first: int | tuple[int, int], last: int | tuple[int, int], iterable: Iterable) -> tuple[str, str]:
    if isinstance(first, tuple):
        f1, f2 = first
        first_number = iterable[f1:f2]
        first_number = DECIMAL_NUMBER_STRINGS[first_number]
    else:
        first_number = iterable[first]

    if isinstance(last, tuple):
        l1, l2 = last
        last_number = iterable[l1:l2]
        last_number = DECIMAL_NUMBER_STRINGS[last_number]
    else:
        last_number = iterable[last]

    return first_number, last_number

if __name__ == "__main__":
    # Part 1 tests
    total_result = 0
    first_func = [is_number]
    last_func = [is_number]

    for test, output in tests['part1']:
        first_index, last_index = find_first_and_last(first_func, last_func, test)
        result = int(test[first_index] + test[last_index])
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
        first_index, last_index = find_first_and_last(first_func, last_func, line)
        part1_solution += int(line[first_index] + line[last_index])

    print(f'Found solution for part 1: {part1_solution}')

    # Part 2 tests
    total_result = 0
    first_func = [is_number, is_string_number]
    last_func = [is_number, is_string_number]

    for test, output in tests['part2']:
        first, last = find_first_and_last(first_func, last_func, test)

        first_number, last_number = indices_to_string(first, last, test)

        result = int(first_number + last_number)
        assert result == output, f"Expected output ({output}), but got result ({result})."
        total_result += result

    assert total_result == PART2_RESULT, \
        f"Expected result of ({PART2_RESULT}), but got result ({total_result})"

    # Part 2 solution
    part2_solution = 0

    for line in puzzle_input.split('\n'):
        first_index, last_index = find_first_and_last(first_func, last_func, line)
        first_number, last_number = indices_to_string(first_index, last_index, line)
        part2_solution += int(first_number + last_number)

    print(f'Found solution for part 2: {part2_solution}')
