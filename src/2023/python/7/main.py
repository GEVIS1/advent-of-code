import os
import re
from collections import Counter

Rank = str
rank_to_value = {
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
            a = rank_to_value[a]

        if not b.isdigit():
            b = rank_to_value[b]

        return int(a) > int(b)
    
    def __lt__(self, other):
        return not self.__gt__(other)
        

class Hand:
    def __init__(self, hand: str):
        self.hand = self.__parse__(hand)

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
            value = rank_to_value[card]
            if value > max_card_value:
                max_card_value, max_card_rank = value, card

        return Card(max_card_rank)

    def result(self):
        hand_counter = Counter(list(self.hand))

        for possible_result in hand_result_precedence:
            result_function = getattr(self, possible_result)
            if result_function(hand_counter):
                return possible_result
        
        return None
    
    def __gt__(self, other):
        a = self.result()
        b = self.result()
        
        if a == b:
            return Card(self.hand[0]) > Card(other.hand[0])
        
        return hand_result_precedence.index(a) < hand_result_precedence.index(b)

    def __lt__(self, other):
        return not self.__gt__(other)

if __name__ == "__main__":
    
    # Part 1 test
    with open(os.path.dirname(__file__) + '/test.txt', encoding='utf-8') as f:
        part1_test_input = f.read()
        part1_test_input = list(filter(''.__ne__, part1_test_input.split('\n')))

    print(f"Five of a kind: {Hand('AAAAA').result()}")
    print(f"Four of a kind: {Hand('AA8AA').result()}")
    print(f"Full house: {Hand('23332').result()}")
    print(f"Three of a kind: {Hand('TTT98').result()}")
    print(f"Two pair: {Hand('23432').result()}")
    print(f"One pair: {Hand('A23A4').result()}")
    print(f"High card: {Hand('23456').result()}")

    print(f"{Hand('T5555') > Hand('J5555') = }")

    part1_test_correct_result = 6440

    # part1_test_races = part1_parse_input(part1_test_input)
    # part1_test_answer = part1_solve_races(part1_test_races)

    # assert part1_test_answer == part1_test_correct_result, \
    #     f"Part 1 test answer was ({part1_test_answer}) " + \
    #         f"where it should be ({part1_test_correct_result})"
