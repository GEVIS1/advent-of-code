import os

def create_translation_map(input_list: list[str]) -> dict[str, dict[int, int]]:
    maps = {}
    map_name = ''

    for string in input_list:
        if 'map:' in string:   
            if map_name:
                maps[map_name] = new_map
            [map_name, _] = string.split(" map:")
            new_map = {}
        else:
            [destination, source, steps] = [int(n) for n in string.split()]
            for step in range(steps):
                new_map[int(source + step)] = int(destination + step)

    # Save the final map
    maps[map_name] = new_map
    return maps

def extract_steps(input_list: list[str]) -> list[str]:
    steps = []
    for string in input_list:
        if 'map:' in string:
            [map_name, _] = string.split(" map:")
            steps.append(map_name)

    return steps

def find_final_seed_locations(almanac: str) -> list[int]:
    translation_steps = extract_steps(almanac)

    [seed_input, *map_input] = almanac
    seeds = [int(n) for n in seed_input.replace("seeds: ", "").split()]
    translation_map = create_translation_map(map_input)

    seed_locations = []
    for seed in seeds:
        seed = int(seed)

        for step in translation_steps:
            seed = translation_map[step].get(seed, seed)

        seed_locations.append(seed)

    return seed_locations
            
if __name__ == "__main__":
    with open(os.path.dirname(__file__) + '/test.txt', encoding='utf-8') as f:
        part1_test_input = f.read()
        part1_test_input = list(filter(''.__ne__, part1_test_input.split('\n')))

    # Run part 1 test
    part1_test_correct_result = 35

    part1_test_result = min(find_final_seed_locations(part1_test_input))
    assert part1_test_result == part1_test_correct_result, \
        f"The lowest location number seed was incorrect. Got ({part1_test_result}), \
            expected ({part1_test_correct_result})"

    # Part 1 solution

    with open(os.path.dirname(__file__) + '/input.txt', encoding='utf-8') as f:
        part1_input = f.read()
        part1_input = list(filter(''.__ne__, part1_input.split('\n')))
    
    part1_result = min(find_final_seed_locations(part1_input))
    
    print(f"Found lowest location number: {part1_result}")