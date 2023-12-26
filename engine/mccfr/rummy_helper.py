from typing import List
from itertools import combinations, chain
from copy import deepcopy


def get_possible_melds(hand: List):
    """" Get all possible melds in hand of 3 and 4 cards\""""

    melds = []
    # Checking possible sequences and groups
    for r in range(3, 4):
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

    # print(hand)
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


def get_card_score(card):
    if int(card[:-1]) > 10:
        return 10
    return 5


def is_hand_melded(hand):
    """Checks if all cards in the hand form a meld"""

    hand2 = deepcopy(hand)
    cards_melded = []
    chosen_melds = []
    for i in range(17):
        melds = get_possible_melds(sort_hand(hand2))

        if len(melds) == 0:
            break

        highest_score = 0
        highest_meld = None
        for meld in melds:
            if calculate_meld_points(meld) > highest_score:
                highest_meld = meld

        if highest_meld is not None:
            chosen_melds.append(highest_meld)
            for card in highest_meld:
                cards_melded.append(card)
                hand2.remove(card)

        if len(flatten(cards_melded)) == len(hand):
            print('all melded')
            return True

    return False


def get_possible_discard_picks(discard_pile_cards=None, hand=None):
    """" Checks possible picks from discard pile, returns a list of dicts with index and the mandatory meld \""""

    for index in range(len(discard_pile_cards)):
        # print(index)
        temp_hand = sort_hand(hand + [discard_pile_cards[index]])
        # print('hand ', hand)
        # print('discard pile ', discard_pile_cards)
        # print('added ', discard_pile_cards[index])
        # print('checking ', temp_hand)
        melds = get_possible_melds(temp_hand)

        for meld in melds:
            if discard_pile_cards[index] in meld:
                # Saving the meld that must be lay, according to rules
                return {
                    'card_index': int(index),
                    'mandatory_meld': meld
                }

    return None


def squash(L):
    if L == []:
        return []
    elif type(L[0]) == type(""):
        M = squash(L[1:])
        M.insert(0, L[0])
        return M
    elif type(L[0]) == type([]):
        M = squash(L[0])
        M.append(squash(L[1:]))
        return M


def flatten(L):
    return [i for i in squash(L) if i != []]
