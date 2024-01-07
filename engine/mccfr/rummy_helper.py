from typing import List
from itertools import combinations, chain
from copy import deepcopy

deck = ['1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '10s', '11s', '12s', '13s',
        '1d', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', '10d', '11d', '12d', '13d',
        '1h', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', '11h', '12h', '13h',
        '1c', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', '10c', '11c', '12c', '13c']


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


def get_card_quality(card, pile):
    pair = 0
    # Checking if it forms pair in hand
    for c in pile:
        # Same rank
        if card[:-1] == c[:-1]:
            pair += 1
            continue
        # One rank up/down and same suit
        if int(card[:-1]) == int(c[:-1]) + 1 and card[-1:] == c[-1:]:
            pair += 1
            continue
        if int(card[:-1]) == int(c[:-1]) - 1 and card[-1:] == c[-1:]:
            pair += 1
            continue

    if pair >= 2:
        return '3'
    elif pair == 1:
        return '2'
    return '1'


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

    # Checking if it forms meld in hand
    for meld in melds:
        if card in meld:
            return '3'

    # Checking if it forms pair in hand
    for c in hand:
        # Same rank
        if card[:-1] == c[:-1]:
            return '2'
        # One rank up/down and same suit
        if int(card[:-1]) == int(c[:-1]) + 1 and card[-1:] == c[-1:]:
            return '2'
        if int(card[:-1]) == int(c[:-1]) - 1 and card[-1:] == c[-1:]:
            return '2'

    # Doesn't form anything
    return '1'


def get_game_stage(hidden_deck_length, own_hand_length=13, opp_hand_length=13):
    """4 = danger, 3 = late, 2 = mid, 1 = early"""
    # print('returning danger ', hidden_deck_length, opp_hand_length, own_hand_length)

    if hidden_deck_length >= 16 and (opp_hand_length >= 9 or own_hand_length >= 9):
        return '1'
    elif hidden_deck_length >= 9 and (opp_hand_length >= 7 or own_hand_length >= 7):
        return '2'
    elif hidden_deck_length >= 4 and (opp_hand_length >= 4 or own_hand_length >= 4):
        return '3'
    elif hidden_deck_length < 4 and (opp_hand_length < 4 or own_hand_length < 4):
        # print('returning danger')
        return '4'

    # If no combination of properties is matched, categorize it based on only in deck length
    if hidden_deck_length >= 16:
        return 1
    elif hidden_deck_length >= 9:
        return 2
    elif hidden_deck_length >= 4:
        return 3
    return 4


def get_hidden_deck_estimation(cpt, current_player, visible_board_data, hidden_deck_length):
    result_dict = {}

    unseen_cards = ['1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '10s', '11s', '12s', '13s',
                    '1d', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', '10d', '11d', '12d', '13d',
                    '1h', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', '11h', '12h', '13h',
                    '1c', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', '10c', '11c', '12c', '13c']

    for card_list in visible_board_data.values():
        for card in card_list:
            if card in unseen_cards:
                unseen_cards.remove(card)

    # Filtering the cpt
    for move in cpt.values():
        for player in move.keys():
            # Get only opp. action
            if player != current_player:
                for action in move[player].keys():
                    if action != 'seen_cards':
                        # Updating card points
                        V = move[player][action]['V']
                        cards = move[player][action]['cards']
                        for card in cards:
                            connections = get_card_connections(card)
                            for conn in connections:
                                curr_v = result_dict.get(conn)
                                if curr_v:
                                    new_V = curr_v + V
                                    result_dict.update({conn: new_V})
                                else:
                                    result_dict.update({conn: V})
                    else:
                        # Updating known cards from opponent, if not already melded
                        if move[player][action] is not None:
                            for card in move[player][action]:
                                if card in unseen_cards:
                                    unseen_cards.remove(card)

    # Getting wanted cards from current hand
    wanted_cards = []
    for card in visible_board_data[f'p{current_player}_cards']:
        connections = get_card_connections(card)
        for conn in connections:
            if conn not in wanted_cards and conn in unseen_cards:
                wanted_cards.append(conn)

    # Counting how many wanted cards are estimated to be in hidden deck
    count = 0
    for card in wanted_cards:
        if card in unseen_cards and result_dict.get(card):
            # Positive points = estimated to be in hidden pile
            if result_dict.get(card) > 0:
                count += 1

    if count >= (hidden_deck_length / 2):
        # 50% has at least 1 point
        return '3'
    elif count >= (hidden_deck_length / 4):
        # 25% has at least 1 point
        return '2'
    return '1'


def get_opp_importance_estimation(cpt, card, current_player):
    result_dict = {}
    for move in cpt.values():
        for player in move.keys():
            # Get only opp. action
            if player != current_player:
                for action in move[player].keys():
                    if action != 'seen_cards':
                        # Updating card points
                        V = move[player][action]['V']
                        cards = move[player][action]['cards']
                        for card in cards:
                            connections = get_card_connections(card)
                            for conn in connections:
                                curr_v = result_dict.get(conn)
                                if curr_v:
                                    new_V = curr_v + V
                                    result_dict.update({conn: new_V})
                                else:
                                    result_dict.update({conn: V})

    v = result_dict.get(card)
    if v is not None:
        if v < 0:
            return '3'
        if v > 0:
            return '1'
    return '2'


def get_card_connections(card):
    suits = ['c', 'h', 's', 'd']

    card_rank = int(card[:-1])
    card_suit = card[-1:]

    connections = [
        f'{card_rank + 1}{card_suit}',  # one rank up,
        f'{card_rank - 1}{card_suit}',  # one rank down,
    ]

    # Adding equal rank of diff suits
    suits.remove(card[-1:])
    for s in suits:
        connections.append(f'{card_rank}{s}')

    for conn in connections:
        if conn[:-1] == '14' or conn[:-1] == '0':
            connections.remove(conn)

    return connections


def get_unseen_cards(board_data):
    return 'inp'


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
        temp_hand = sort_hand(hand + discard_pile_cards[index:])
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
