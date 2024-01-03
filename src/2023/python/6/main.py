import os
from functools import reduce

Time = int
Distance = int
Race = tuple[Time, Distance]

def parse_input(race_data: str) -> list[Race]:
    [times, distances] = race_data
    [_, times] = times.split("Time:")
    [_, distances] = distances.split("Distance:")
    times = string_to_ints(times)
    distances = string_to_ints(distances)
    races = []

    for i, (time, distance) in enumerate(zip(times,distances)):
        races.append((time, distance))

    return races

def string_to_ints(int_string: str) -> list[int]:
    ints = []
    new_int = ''

    for c in int_string:
        if c.isdigit():
            new_int += c
        else:
            if new_int:
                ints.append(int(new_int))
            new_int = ''

    if new_int:
        ints.append(int(new_int))

    return ints

def calculate_distance_from_button_press(button_pressed_milliseconds: int, race_time_milliseconds: int) -> int:
    time_left_to_race = race_time_milliseconds - button_pressed_milliseconds

    assert time_left_to_race >= 0, "Can not hold button longer than race time"

    return button_pressed_milliseconds * time_left_to_race

def part1_solve_races(races: list[Race]) -> int:
    race_solutions = []

    for race in races:
        time, distance = race
        winning_solutions = 0

        for attempt in range(time + 1):
            distance_achieved = calculate_distance_from_button_press(attempt, time)
            if distance_achieved > distance:
                winning_solutions += 1

        race_solutions.append(winning_solutions)

    answer = reduce(lambda x, y: x*y, race_solutions)
    return answer

if __name__ == "__main__":
    
    # Part 1 test
    
    with open(os.path.dirname(__file__) + '/test.txt', encoding='utf-8') as f:
        part1_test_input = f.read()
        part1_test_input = list(filter(''.__ne__, part1_test_input.split('\n')))

    part1_test_correct_result = 288

    part1_test_races = parse_input(part1_test_input)
    part1_test_answer = part1_solve_races(part1_test_races)

    assert part1_test_answer == part1_test_correct_result, \
        f"Part 1 test answer was ({part1_test_answer}) " + \
            f"where it should be ({part1_test_correct_result})"
    
    # Part 1 solution
    with open(os.path.dirname(__file__) + '/input.txt', encoding='utf-8') as f:
        part1_input = f.read()
        part1_input = list(filter(''.__ne__, part1_input.split('\n')))
    
    part1_races = parse_input(part1_input)
    part1_answer = part1_solve_races(part1_races)

    print(f"Found solution to part 1: {part1_answer}")
    