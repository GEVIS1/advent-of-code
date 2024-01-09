import os
import re
from collections import Counter
from functools import cmp_to_key

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
        b = other.result()
        
        # Tie-breaker
        if a == b:
            print(f"a ({self.hand}) ({a}) is the same as b ({other.hand}) ({b})")
            card_index = 0
            hand_a_card = rank_to_value[self.hand[card_index]]
            hand_b_card = rank_to_value[other.hand[card_index]]
            print(f"Hand A card {card_index}: {hand_a_card}. Hand B card {card_index}: {hand_b_card}")
            while hand_a_card == hand_b_card:
                print("Top of while loop:")
                card_index += 1
                hand_a_card = rank_to_value[self.hand[card_index]]
                hand_b_card = rank_to_value[other.hand[card_index]]
                print(f"Hand A card {card_index}: {hand_a_card}. Hand B card {card_index}: {hand_b_card}")
                
            print(f"{hand_a_card=}\n{hand_b_card=}")
            print(f"Returning {hand_a_card > hand_b_card =}")
            return hand_a_card > hand_b_card
        
        print(f"{hand_result_precedence.index(a) < hand_result_precedence.index(b) = }")

        return hand_result_precedence.index(a) < hand_result_precedence.index(b)

    def __lt__(self, other):
        return not self.__gt__(other)

def sort_hands(hands: list[Hand]) -> list[Hand]:
    hands_are_sorted = False
    sorted_hands = hands.copy()
    len_list = len(sorted_hands)

    while not hands_are_sorted:
        print("Top of while sorted loop")
        hands_are_sorted = True
        
        for i in range(len_list):
            print(f"Top of range loop on i = {i}")
            end_of_list = i == len_list - 1
            print(f"{end_of_list=}")
            if not end_of_list and sorted_hands[i] > sorted_hands[i+1]:
                hands_are_sorted = False
                print(f"Swapping {sorted_hands[i]} with {sorted_hands[i+1]}")
                sorted_hands[i], sorted_hands[i+1] = sorted_hands[i+1], sorted_hands[i]

    return sorted_hands

if __name__ == "__main__":
    
    # Part 1 test
    with open(os.path.dirname(__file__) + '/test.txt', encoding='utf-8') as f:
        part1_test_input = f.read()
        part1_test_input = list(filter(''.__ne__, part1_test_input.split('\n')))

    part1_test_correct_result = 6440

    # part1_test_races = part1_parse_input(part1_test_input)
    # part1_test_answer = part1_solve_races(part1_test_races)

    part1_test_hands = []
    part1_test_bids = []

    for line in part1_test_input:
        [hand, bid] = line.split(' ')
        part1_test_hands.append(hand)
        part1_test_bids.append(bid)

    part1_test_hands_sorted = sort_hands(part1_test_hands)

    print(f"part1_test_hands_sorted=\t{part1_test_hands_sorted}")

    correct_order = [
        "32T3K",
        "KTJJT",
        "KK677",
        "T55J5",
        "QQQJA", 
    ]

    print(f"correct_order=\t\t\t{correct_order}")

    # print(f"{Hand('32T3K') < Hand('KTJJT')=}")
    # print(f"{Hand('KTJJT') < Hand('KK677')=}")
    # print(f"{Hand('KK677') < Hand('T55J5')=}")
    # print(f"{Hand('T55J5') < Hand('QQQJA')=}")
    # print(f"{Hand('QQQJA') > Hand('T55J5')=}") 
    # print(f"{Hand('KTJJT') > Hand('KK677')=}")
    # assert part1_test_answer == part1_test_correct_result, \
    #     f"Part 1 test answer was ({part1_test_answer}) " + \
    #         f"where it should be ({part1_test_correct_result})"
