import os
import re

def load_input(path: str) -> str:
    with open(os.path.dirname(__file__) + "/" + path, encoding='utf-8') as f:
        file_input = f.read()
        file_input = list(filter(''.__ne__, file_input.split('\n')))
    
    return file_input

if __name__ == "__main__":
    # Part 1 test
    part1_test_input = load_input('./test.txt')

    part1_test_tests = []
    
    for line in part1_test_input:
        if re.match(r'\[test.*\]', line):
            print("Found test header:", line)
