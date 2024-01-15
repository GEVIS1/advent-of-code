import os

pipe_to_movement = {
    "north": {
        "|": ( 0, -1),
        "L": ( 1,  0),
        "J": (-1,  0),
    },
    "east": {
        "L": ( 0,  1),
        "-": (-1,  0),
        "F": ( 0, -1),
    },
    "south": {
        "F": ( 1,  0),
        "|": ( 0,  1),
        "7": (-1,  0),
    },
    "west": {
        "-": ( 1,  0),
        "7": ( 0, -1),
        "J": ( 0,  1),
    },
}

def load_input(path: str) -> list[str]:
    with open(os.path.dirname(__file__) + "/" + path, encoding='utf-8') as f:
        file_input = f.read()
        file_input = list(filter(''.__ne__, file_input.split('\n')))
    
    return file_input

def follow_path(tiles: list[str]) -> list[str]:
    path_distances = []
    
    for y, row in enumerate(tiles):
        for x, col in enumerate(row):
            print(col, end='')

        print()

def find_start(tiles: list[str]) -> tuple[int]:
    for y, row in enumerate(tiles):
        for x, col in enumerate(row):
            if col == "S":
                return (x,y)

if __name__ == "__main__":
    # Part 1 test
    part1_test_input = load_input('./test.txt')
    
    for line in part1_test_input:
        print(line)

    start_indices = find_start(part1_test_input)

    print(start_indices)