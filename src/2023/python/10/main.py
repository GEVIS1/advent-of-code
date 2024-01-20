import os
from collections import deque

# pipe_exits = {
#         "|": ( 0, -1),
#         "L": ( 1,  0),
#         "J": (-1,  0),
#         "-": (-1,  0),
#         "F": ( 0, -1),
#         "7": (-1,  0),
# }

directions = {
    "north": ( 0, -1),
    "east":  ( 1,  0),
    "south": ( 0,  1),
    "west":  (-1,  0)
}

pipe_to_movement = {
    "north": {
        "|": ( 0, -1),
        "F": ( 1,  0),
        "7": (-1,  0),
    },
    "east": {
        "J": ( 0, -1),
        "-": ( 1,  0),
        "7": ( 0,  1),
    },
    "south": {
        "|": ( 0,  1),
        "L": ( 1,  0),
        "J": (-1,  0),
    },
    "west": {
        "L": ( 0, -1),
        "-": (-1,  0),
        "F": ( 0,  1),
    },
}

def load_input(path: str) -> list[str]:
    with open(os.path.dirname(__file__) + "/" + path, encoding='utf-8') as f:
        file_input = f.read()
        file_input = list(filter(''.__ne__, file_input.split('\n')))
    
    return file_input

def follow_path(tiles: list[str]) -> list[str]:
    path_distances = [["." for c in row] for row in tiles]
    
    start_indices = find_start(tiles)
    start_col, start_row = start_indices
    current_indices = start_indices
    ran_once = False
    steps_taken = 0
    path_distances[start_row][start_col] = str(steps_taken)
    tile_deque = deque()

    while len(deque):
        ran_once = True
        possible_directions = find_possible_directions(tiles, current_indices)

        # if len(possible_directions) == 1:
        #     col, row = possible_directions[0][2]

        #     # TODO: This naive solution breaks on the actual input.
        #     # We need a better way to determine if we are at the end.
        #     if tiles[row][col] == "S":
        #         break

        # Remove "S" if we didn't break.
        # possible_directions = list(filter(lambda item: item[1] != "S", possible_directions))

        # Use a deque and visit all possible locations

        for direction, tile, indices in possible_directions:
            curr_col, curr_row = current_indices 
            move_col, move_row = indices
            already_visited_tile = path_distances[move_row][move_col] != "."
            
            if not already_visited_tile or indices == start_indices:
                #calculated_distance = (abs(move_col - start_col) + abs(move_row - start_row))
                steps_taken += 1
                path_distances[move_row][move_col] = str(steps_taken) # TODO: Make int?
                current_indices = indices
                break

    return path_distances

def path_distance_centering(path_distances: list[str]) -> list[str|int]:
    max_distance = max(int(c) if c != "." else -1 for sub in path_distances for c in sub)
    new_max_distance = max_distance // 2
    new_path_distances = path_distances.copy()

    for row, row_list in enumerate(new_path_distances):
        for col, char in enumerate(row_list):
            if (char != ".") and (char_as_int := int(char)) > new_max_distance:
                new_path_distances[row][col] = char_as_int - new_max_distance

    return new_path_distances

def find_start(tiles: list[str]) -> tuple[int]:
    for y, row in enumerate(tiles):
        for x, col in enumerate(row):
            if col == "S":
                return (x,y)
            
def find_possible_directions(tiles: list[str], cur_pos: tuple[int, int]) -> list[tuple[int,int]]:
    possible_directions = []
    max_row = len(tiles)
    max_col = len(tiles[0])
    col, row = cur_pos

    for direction in directions:
        x, y = directions[direction]
        next_row = row + y
        next_col = col + x

        # Make sure we don't overstep the list
        if 0 <= next_col < max_col and 0 <= next_row < max_row:
            adjacent_tile = tiles[row + y][col + x]
            indices = col + x, row + y
            if adjacent_tile in pipe_to_movement[direction] or adjacent_tile == "S":
                possible_directions.append((direction, adjacent_tile, indices))

    return possible_directions

def find_max_distance(tiles: list[int|str]) -> int:
    return max(n if isinstance(n, int) else -1 for sub in tiles for n in sub)

if __name__ == "__main__":
    # Part 1 test
    part1_test_expected_result = 8
    part1_test_input = load_input('./test.txt')
    
    part1_test_path_distances = follow_path(part1_test_input)

    part1_test_formatted_distances = path_distance_centering(part1_test_path_distances)
    part1_test_result = find_max_distance(part1_test_formatted_distances)
    assert part1_test_result == part1_test_expected_result, f"Expected {part1_test_expected_result}, but got {part1_test_result}"

    # Part 1 solution
    part1_solution_input = load_input('./input.txt')
    part1_solution_path_distances = follow_path(part1_solution_input)
    part1_solution_formatted_distances = path_distance_centering(part1_solution_path_distances)
    part1_solution_result = find_max_distance(part1_solution_formatted_distances)

    print(f"Part 1 solution found: {part1_solution_result}")