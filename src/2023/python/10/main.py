import os
import time

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

    while current_indices != start_indices or not ran_once:
        for line in tiles:
            print(line)
        for line in path_distances:
            print(line)

        ran_once = True
        possible_directions = find_possible_directions(tiles, current_indices)

        if len(possible_directions) == 1:
            col, row = possible_directions[0][2]
            if tiles[row][col] == "S":
                break

        # print(f"I'm currently on the tile ({tiles[start_indices[1]][start_indices[0]]}) at col: {start_indices[1]} row: {start_indices[0]}")
        # print("My possible directions are:")
        for direction, tile, indices in possible_directions:
            curr_col, curr_row = current_indices 
            move_col, move_row = indices
            already_visited_tile = path_distances[move_row][move_col] != "."
            
            if not already_visited_tile or indices == start_indices:
                # print(f"Picking {direction} and moving to a \'{tile}\' tile.")
                # print(f"This moves us from col: {curr_col} row: {curr_row} to col: {move_col} row: {move_row}.")
                #calculated_distance = (abs(move_col - start_col) + abs(move_row - start_row))
                # print(f"{calculated_distance=}")
                steps_taken += 1
                path_distances[move_row][move_col] = str(steps_taken) # TODO: Make int
                print(f"Setting ({current_indices}) to ({indices})")
                current_indices = indices
                break

    return path_distances

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

if __name__ == "__main__":
    # Part 1 test
    part1_test_input = load_input('./test.txt')
    
    path_distances = follow_path(part1_test_input)

    
