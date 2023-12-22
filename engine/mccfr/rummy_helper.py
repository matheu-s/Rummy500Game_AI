from typing import List
from itertools import combinations


def get_possible_melds(hand: List):
    """" Get all possible melds in p0 hand\""""

    melds = []
    # Checking possible sequences and groups
    for r in range(3, len(hand) + 1):
        for comb in combinations(hand, r):
            comb = list(comb)
            if is_meld(comb):
                melds.append(comb)

    return melds


def is_seq(cards):
    for ind in range(1, len(cards)):
        if cards[ind - 1][-1:] != cards[ind][-1:]:
            return False
        if int(cards[ind - 1][:-1]) != int(cards[ind][:-1]) - 1:
            return False
    return True


def is_group(cards):
    for ind in range(1, len(cards)):
        if cards[ind - 1][:-1] != cards[ind][:-1]:
            return False
    return True


def is_meld(cards):
    """" Checks if provided combination is a meld \""""

    return is_seq(cards) or is_group(cards)


def calculate_meld_points(meld):
    """" Calculates points of a meld combination \""""

    points = 0
    for card in meld:
        if int(card[:-1]) > 10:
            points += 10
            continue
        points += 5

    return points


def sort_hand(hand):
    """" Returns the hand sorted\""""

    cards_dict = {
        's': [],
        'h': [],
        'c': [],
        'd': []
    }

    for i in hand:
        cards_dict[i[-1:]].append(int(i[:-1]))

    cards_dict['s'].sort()
    cards_dict['h'].sort()
    cards_dict['c'].sort()
    cards_dict['d'].sort()

    sorted_cards = []
    for suit in cards_dict:
        for i in cards_dict[suit]:
            sorted_cards.append(str(i) + suit)

    return sorted_cards


def is_meld_former(card, hand):
    """" Checks if new card will form any meld or connect to existing ones, 1 = true, 2 = false\""""

    temp_hand = hand + [card]
    melds = get_possible_melds(temp_hand)

    for meld in melds:
        if card in meld:
            return '1'

    return '2'
