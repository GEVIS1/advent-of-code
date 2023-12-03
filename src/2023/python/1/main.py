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

    ]
}

part1_result = 142
part2_result = 0

def find_first_and_last(first: callable, last: callable, iterable: Iterable) -> tuple[int, int]:
    match iterable:
        case l if type(iterable) == type(str()):
            i1 = 0
            i2 = len(l) - 1
            found = False

            while not found:
                current_first = l[i1]
                correct_first = first(current_first)
                
                current_last  = l[i2]
                correct_last  = first(current_last)

                if not correct_first:
                    i1 += 1
                if not correct_last:
                    i2 -= 1

                if correct_first and correct_last:
                    found = True 
                elif i1 > i2 or i2 < i1:
                    raise RuntimeError("Indices converged at centre and no first and last values were found.")
        case _:
            raise NotImplementedError(f"{type(iterable)} support not implemented")

    return (i1, i2)

def is_number(n: str) -> bool:
    try:
        type(int(n)) == type(int)
    except:
        return False
    
    return True

if __name__ == "__main__":
    # Run tests
    total_result = 0
    first_func = is_number
    last_func = is_number

    for test, output in tests['part1']:
        first, last = find_first_and_last(first_func, last_func, test)
        result = int(test[first] + test[last])
        assert result == output, "Expected output ({output}), but got result ({result})."
        total_result += result
    
    assert total_result == part1_result, "Expected result of  ({part1_result}), but got result ({total_result})"

    # Load input
    with open(os.path.dirname(__file__) + '/input.txt') as f:
        puzzle_input = f.read()
    part1_solution = 0

    for line in puzzle_input.split('\n'):
        first, last = find_first_and_last(first_func, last_func, line)
        part1_solution += int(line[first] + line[last])

    print(f'Found solution to part 1: {part1_solution}')