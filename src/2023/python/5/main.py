import os
from math import inf

def create_translation_map(input_list: list[str]) -> dict[int, int]:
    translation_map = {}
    for string in input_list:
        [destination, source, steps] = [int(n) for n in string.split()]
        for step in range(steps):
            translation_map[int(source + step)] = int(destination + step)

    return translation_map

def extract_step_names(input_list: list[str]) -> list[str]:
    steps = []
    for string in input_list:
        if 'map:' in string:
            [map_name, _] = string.split(" map:")
            steps.append(map_name)

    return steps

def extract_step_data(input_list: list[str]) -> list[list[str]]:
    all_steps = []
    steps = []

    for line in input_list:
        if 'map:' in line:
            if steps:
                all_steps.append(steps)
            steps = []
        else:
            steps.append(line)

    all_steps.append(steps)

    print(all_steps)

    return all_steps
        

def find_final_seed_location(almanac: str) -> int:
    translation_steps = extract_step_names(almanac)

    [seed_input, *map_input] = almanac
    seeds = [int(n) for n in seed_input.replace("seeds: ", "").split()]
    translation_data = extract_step_data(map_input)

    print("Hi")
    best_location = inf

    print(f"{ best_location =}")
    for seed in seeds:
        seed = int(seed)

        print(f"Seed: {seed}")

        for i, data in enumerate(translation_data):
            print(i)
            print(data)
            translation_map = create_translation_map(data)
            original_seed = seed
            seed = translation_map.get(seed, seed)
            print(f"\tStep: {translation_steps[i]}\n\t{original_seed} => {seed}")

        if seed < best_location:
            best_location = seed
            print(f"New best location: {best_location}")

    return best_location
            
if __name__ == "__main__":
    with open(os.path.dirname(__file__) + '/test.txt', encoding='utf-8') as f:
        part1_test_input = f.read()
        part1_test_input = list(filter(''.__ne__, part1_test_input.split('\n')))

    # Run part 1 test
    part1_test_correct_result = 35

    part1_test_result = find_final_seed_location(part1_test_input)
    assert part1_test_result == part1_test_correct_result, \
        f"The lowest location number seed was incorrect. Got ({part1_test_result}), \
            expected ({part1_test_correct_result})"

    print("Test finished")

    # Part 1 solution
    print("Reading input.txt")
    with open(os.path.dirname(__file__) + '/input.txt', encoding='utf-8') as f:
        part1_input = f.read()
        part1_input = list(filter(''.__ne__, part1_input.split('\n')))
    
    print("Solving part1")
    part1_result = find_final_seed_location(part1_input)
    
    print(f"Found lowest location number: {part1_result}")