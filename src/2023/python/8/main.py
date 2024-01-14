import os
import re

def load_input(path: str) -> list[str]:
    with open(os.path.dirname(__file__) + "/" + path, encoding='utf-8') as f:
        file_input = f.read()
        file_input = list(filter(''.__ne__, file_input.split('\n')))
    
    return file_input

def parse_input(input_list: list[str]) -> [str, str]:
    instructions = input_list.pop(0)

    return [instructions, input_list]

def create_generator(instructions: str):
    i = 0
    bounds = len(instructions)
    while True:
        yield instructions[i]
        i = (i + 1) % bounds

class Node:
    def __init__(self, key = None, left = None, right = None):
        self._key = key
        self._left = left
        self._right = right

    @property
    def key(self):
        return self._key
    
    @key.setter
    def key(self, value):
        self._key = value

    @property
    def left(self):
        return self._left
    
    @left.setter
    def left(self, value):
        self._left = value

    @property
    def right(self):
        return self._right
    
    @right.setter
    def right(self, value):
        self._right = value
    
def construct_nodes(nodes: list[str]) -> Node:
    node_dict = {}

    # This could be made recursive, but here we just instantiate all nodes and then update links in a second pass
    for node_recipe in nodes:
        (node, _, _) = re.search(r'([A-Z]{3}).*([A-Z]{3}).*([A-Z]{3})', node_recipe).groups()
        node_dict[node] = Node(node)

    for node_recipe in nodes:
        (node, left, right) = re.search(r'([A-Z]{3}).*([A-Z]{3}).*([A-Z]{3})', node_recipe).groups()
        node_dict[node].left = node_dict[left]
        node_dict[node].right = node_dict[right]

    return node_dict["AAA"]

def follow_steps(instructions: str, nodes: list[str]) -> int:
    current_node = construct_nodes(nodes)
    instructions = create_generator(instructions)

    MAX_ITER = 1000000
    steps = 0
    for instr in instructions:
        if current_node.key == "ZZZ" or steps > MAX_ITER:
            break

        match (instr):
            case ("L"):
                current_node = current_node.left
            case ("R"):
                current_node = current_node.right
            case (_):
                raise ValueError(f"Incorrect instruction ({instr})")
        
        steps += 1

    if steps > MAX_ITER:
        raise OverflowError(f'Hit MAX_ITER limit ({MAX_ITER})')

    return steps

if __name__ == "__main__":
    # Part 1 test
    part1_test1_input = load_input('./test1.txt')
    part1_test2_input = load_input('./test2.txt')

    for [test, result] in [[part1_test1_input, 2], [part1_test2_input, 6]]:
        [instructions, nodes] = parse_input(test)
        steps = follow_steps(instructions, nodes)
        assert steps == result, f"Expected steps to be ({result}), but got ({steps})."

    # Part 1 solution
    part1_solution_input = load_input('./input.txt')
    [part1_solution_instructions, part1_solution_nodes] = parse_input(part1_solution_input)
    print(f"{part1_solution_instructions = }")
    part1_solution_answer = follow_steps(part1_solution_instructions, part1_solution_nodes)
    print(f"Part 1 solution: {part1_solution_answer}")

