import os
import re

Rank = str

class Card:
    rank_to_value = {
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14
}
    def __init__(self, r: Rank):
        self.rank = self.__parse__(r)

    def __parse__(self, r: Rank):
        r = r.upper()

        if re.match(r'[0-9TJKQA]', r):
            print(f"{r} is valid")
            return r
        
        raise ValueError(f"Invalid Card: {r}")
        
    def __gt__(self, other):
        a = self.rank
        b = other.rank

        if not a.isdigit():
            a = self.rank_to_value[a]

        if not b.isdigit():
            b = self.rank_to_value[b]

        print(f"{a = } {b = }")
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

    def is_pair(self):
        

def decide_stronger_hand(a: Hand, b: Hand) -> Hand:
    
    pass

if __name__ == "__main__":
    
    # Part 1 test
    with open(os.path.dirname(__file__) + '/test.txt', encoding='utf-8') as f:
        part1_test_input = f.read()
        part1_test_input = list(filter(''.__ne__, part1_test_input.split('\n')))

    hand_a = Hand('32T3K')

    print(f"{hand_a.hand=}")

    part1_test_correct_result = 6440

    # part1_test_races = part1_parse_input(part1_test_input)
    # part1_test_answer = part1_solve_races(part1_test_races)

    # assert part1_test_answer == part1_test_correct_result, \
    #     f"Part 1 test answer was ({part1_test_answer}) " + \
    #         f"where it should be ({part1_test_correct_result})"
