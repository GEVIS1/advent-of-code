import os
import re
from collections import Counter

def load_input(path: str) -> str:
    with open(os.path.dirname(__file__) + "/" + path, encoding='utf-8') as f:
        file_input = f.read()
        file_input = list(filter(''.__ne__, file_input.split('\n')))
    
    return file_input

Rank = str
hand_result_precedence = [
    "five_of_a_kind",
    "four_of_a_kind",
    "full_house",
    "three_of_a_kind",
    "two_pairs",
    "one_pair",
    "high_card",
]

class Card:
    def __init__(self, r: Rank = 'A'):
        self.rank = self.__parse__(r)

    def __parse__(self, r: Rank):
        r = r.upper()

        if re.match(r'[0-9TJKQA]', r):
            return r
        
        raise ValueError(f"Invalid Card: {r}")
        
    def __gt__(self, other):
        a = self.rank
        b = other.rank

        if not a.isdigit():
            a = self.rank_to_value[a]

        if not b.isdigit():
            b = self.rank_to_value[b]

        return int(a) > int(b)
    
    def __lt__(self, other):
        return not self.__gt__(other)
        

class Hand:
    modes = {
        "part1": 1,
        "part2": 2,
    }
    part1_rank_to_value = {
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "T": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14
    }
    part2_rank_to_value = {
        "J": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "T": 10,
        "Q": 12,
        "K": 13,
        "A": 14
}

    def __init__(self, hand: str, bid: int, mode="part1"):
        self.mode = self.verify_mode(mode)
        self.rank_to_value = self.part1_rank_to_value if self.mode == "part1" else self.part2_rank_to_value
        self.hand = self.__parse__(hand)
        self.bid = bid

    # This seems unnecessary
    def verify_mode(self, mode: str):
        if mode not in self.modes:
            raise ValueError("Incorrect mode selection.")

        return mode

    def __parse__(self, hand: str):
        if len(hand) != 5:
            raise ValueError("Hand must be 5 cards long")

        for c in hand:
            Card(c)
            
        return hand.upper()

    def full_house(self, hand_counter: Counter):
        values = hand_counter.values()
        return 3 in values and 2 in values

    def five_of_a_kind(self, hand_counter: Counter):
        values = hand_counter.values()
        return 5 in values
    
    def four_of_a_kind(self, hand_counter: Counter):
        values = hand_counter.values()
        return 4 in values
    
    def three_of_a_kind(self, hand_counter: Counter):
        values = hand_counter.values()
        return 3 in values
    
    def two_pairs(self, hand_counter: Counter):
        values = hand_counter.values()
        return Counter(values)[2] == 2
    
    def one_pair(self, hand_counter: Counter):
        values = hand_counter.values()
        return 2 in values
    
    def high_card(self, hand_counter: Counter = None):
        if not hand_counter:
            hand_counter = Counter(list(self.hand))
        
        max_card_value = 0
        max_card_rank = None

        for card in hand_counter.keys():
            value = self.rank_to_value[card]
            if value > max_card_value:
                max_card_value, max_card_rank = value, card

        return Card(max_card_rank)

    def result(self):
        hand_counter = Counter(list(self.hand))

        for possible_result in hand_result_precedence:
            result_function = getattr(self, possible_result)

            # For part 2 convert the jack to achieve better result
            if self.mode == "part2" and "J" in hand_counter:
                # This is naive and should be tested properly
                most_represented_card, _  = max(hand_counter.items(), key=lambda i: i[1])
                jokered_hand_counter = hand_counter.copy()
                jokered_hand_counter[most_represented_card] += 1
                del jokered_hand_counter["J"]

                print(f"Joker rule triggered:\n{hand_counter=}\n{jokered_hand_counter=}")
                if result_function(jokered_hand_counter):
                    return possible_result

            elif result_function(hand_counter):
                return possible_result
        
        return None
    
    def __gt__(self, other):
        a = self.result()
        b = other.result()
        
        # Tie-breaker
        if a == b:

            card_index = 0
            hand_a_card = self.rank_to_value[self.hand[card_index]]
            hand_b_card = self.rank_to_value[other.hand[card_index]]

            while hand_a_card == hand_b_card:
    
                card_index += 1
                hand_a_card = self.rank_to_value[self.hand[card_index]]
                hand_b_card = self.rank_to_value[other.hand[card_index]]
    
            return hand_a_card > hand_b_card
        

        return hand_result_precedence.index(a) < hand_result_precedence.index(b)

    def __lt__(self, other):
        return not self.__gt__(other)
    
    def __eq__(self, other):
        sort_fn = lambda s: "".join(sorted(s))

        a = sort_fn(self.hand)
        b = sort_fn(other.hand)

        return a == b

    def __repr__(self):
        return f"\'{self.hand}\'"

def parse_input(input_str: list[str], mode="part1") -> list[Hand]:
    hands = []

    for line in input_str:
        [hand, bid] = line.split(' ')
        hands.append(Hand(hand, int(bid), mode))
    
    return hands

def calculate_sum(sorted_hands: list[Hand]):
    return sum(h.bid * (i + 1) for i,h in enumerate(sorted_hands))

if __name__ == "__main__":
    
    # Part 1 test
    part1_test_input = load_input('./test.txt')
    part1_test_correct_result = 6440

    # part1_test_races = part1_parse_input(part1_test_input)
    # part1_test_answer = part1_solve_races(part1_test_races)

    part1_test_hands = parse_input(part1_test_input, "part1")
    part1_test_hands_sorted = sorted(part1_test_hands)

    part1_test_answer = calculate_sum(part1_test_hands_sorted)

    assert part1_test_answer == part1_test_correct_result, \
        f"Part 1 test answer was ({part1_test_answer}) " + \
            f"where it should be ({part1_test_correct_result})"

    # Part 1 solution
    part1_solution_input = load_input('./input.txt')
    part1_solution_hands = parse_input(part1_solution_input, "part1")
    part1_solution_hands_sorted = sorted(part1_solution_hands)
    part1_solution_answer = calculate_sum(part1_test_hands_sorted)

    print(f"Part 1 solution found: {part1_solution_answer}")

    # Part 2 test
    part2_test_correct_result = 5905
    part2_test_input = load_input('./test.txt')
    part2_test_hands = parse_input(part2_test_input, "part2")
    part2_test_hands_sorted = sorted(part2_test_hands)
    part2_test_answer = calculate_sum(part2_test_hands_sorted)

    assert part2_test_answer == part2_test_correct_result, \
        f"Part 2 test answer was ({part2_test_answer}) " + \
            f"where it should be ({part2_test_correct_result})"