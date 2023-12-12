import random
from typing import List, cast, Dict
from random import shuffle
from labml_nn.cfr import History as _History, InfoSet as _InfoSet, Action, Player, CFRConfigs
from engine.mccfr.infoset import InfoSet
from engine.mccfr.rummy_helper import get_possible_melds, calculate_meld_points, sort_hand
from copy import deepcopy

# There are two players
PLAYERS = cast(List[Player], [0, 1])

# The three cards in play are Ace, King and Queen
CHANCES = cast(List[Action], ['1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '10s', '11s', '12s', '13s',
                              '1d', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', '10d', '11d', '12d', '13d',
                              '1h', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', '11h', '12h', '13h',
                              '1c', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', '10c', '11c', '12c', '13c'])


class History(_History):
    # History
    history = ''
    p0_cards = []
    p1_cards = []
    p0_points = 0
    p1_points = 0
    discard_pile = []
    hidden_deck = []
    # TODO: Implement original cards, to keep track of same infoset from beginning
    # TODO: Implement original points, to keep already existing points, vantage

    def __init__(self, history: str = '', data: Dict = None):
        """
        Initialize with a given history string
        """
        self.history = history

        if data is not None:
            self.p0_cards = data['p0_cards']
            self.p1_cards = data['p1_cards']
            self.p0_points = data['p0_points']
            self.p1_points = data['p1_points']
            self.discard_pile = data['discard_pile']
            self.hidden_deck = data['hidden_deck']

    def is_terminal(self):
        """
        Whether the history is terminal (less than 3 moves ahead, after 13 cards dealt).
        """
        return len(self.history) == 3

    def _terminal_utility_p0(self) -> float:
        """
        Calculate the terminal utility for player 0
        """
        self.calculate_points()
        return self.p0_points - self.p1_points

    def terminal_utility(self, i: Player) -> float:
        """
        Get the terminal utility for player $i$
        """
        # If is Player 0
        if i == PLAYERS[0]:
            return self._terminal_utility_p0()
        # Otherwise, $u_2(z) = -u_1(z)$
        else:
            return -1 * self._terminal_utility_p0()

    def is_chance(self) -> bool:
        """If cards were not dealt yet"""
        return len(self.p0_cards) == 0 or len(self.p1_cards) == 0

    def __add__(self, other: Action):
        """
        Add an action to the history and return a new history
        """
        data = {
            'p0_cards': self.p0_cards,
            'p1_cards': self.p1_cards,
            'p0_points': self.p0_points,
            'p1_points': self.p1_points,
            'discard_pile': self.discard_pile,
            'hidden_deck': self.hidden_deck
        }

        if other == 'd':
            self.draw_discard()
        elif other == 'h':
            self.draw_hidden()

        return History(self.history + other, data)

    def draw_discard(self):
        card = self.discard_pile.pop()
        if self.player() == 0:
            self.p0_cards.append(card)
        else:
            self.p1_cards.append(card)
        self.discard()

    def draw_hidden(self):
        card = self.hidden_deck.pop()
        if self.player() == 0:
            self.p0_cards.append(card)
        else:
            self.p1_cards.append(card)
        self.discard()

    def discard(self):
        """Discard a card that doesn't form a meld, otherwise random"""

        # Getting hand
        if self.player() == 0:
            hand = deepcopy(self.p0_cards)
        else:
            hand = deepcopy(self.p1_cards)

        # Saves all cards that form melds
        meld_cards = []
        melds = get_possible_melds(hand)
        for meld in melds:
            for card in meld:
                if card not in meld_cards:
                    meld_cards.append(card)

        # Chooses the first card from hand that did not form any meld
        chosen_card = None
        for card in hand:
            if card not in meld_cards:
                chosen_card = card
                # If none was found, chooses random
        if chosen_card is None:
            chosen_card = random.choice(hand)

        # Removes card from hand
        if self.player() == 0:
            self.p0_cards.remove(chosen_card)
        else:
            self.p1_cards.remove(chosen_card)

        # Adds card to discard pile
        self.discard_pile.append(chosen_card)

    def calculate_points(self):
        """Calculates points of best melds in hand, set self points"""

        dict_melds = {
            'p0_melds': [],
            'p1_melds': []
        }

        copy_p0_cards = deepcopy(self.p0_cards)
        copy_p1_cards = deepcopy(self.p1_cards)

        for hand in [self.p0_cards, self.p1_cards]:
            sorted_hand = sort_hand(hand)
            # Max melds possible 17
            for i in range(17):
                melds = get_possible_melds(sort_hand(sorted_hand))

                if len(melds) == 0:
                    break

                highest_score = 0
                highest_meld = None
                for meld in melds:
                    if calculate_meld_points(meld) > highest_score:
                        highest_meld = meld

                if highest_meld is not None:
                    if hand == copy_p0_cards:
                        dict_melds['p0_melds'].append(highest_meld)
                        for card in highest_meld:
                            sorted_hand.remove(card)
                    else:
                        dict_melds['p1_melds'].append(highest_meld)
                        for card in highest_meld:
                            sorted_hand.remove(card)

        for meld in dict_melds['p0_melds']:
            self.p0_points += calculate_meld_points(meld)
        for meld in dict_melds['p1_melds']:
            self.p1_points += calculate_meld_points(meld)

    def player(self) -> Player:
        """
        Current player
        """
        return cast(Player, len(self.history) % 2)

    def sample_chance(self) -> Action:
        """
        Deal cards
        """

        # Shuffling
        card_list = CHANCES
        shuffle(card_list)

        # Dealing cards to players
        self.p0_cards = card_list[-13:]
        card_list = card_list[:-13]
        self.p1_cards = card_list[-13:]
        card_list = card_list[:-13]

        # Flipping discard pile card
        self.discard_pile.append(card_list.pop())

        # Saving hidden deck
        self.hidden_deck = card_list

        return

    def __repr__(self):
        """
        Human readable representation
        """
        return repr(self.history)

    def info_set_key(self) -> str:
        """
        Information set key for the current history.
        This is a string of actions only visible to the current player.
        """
        # Get current player
        i = self.player()
        # Current player sees her card and the actions
        # TODO: think...make more static?
        if i == 0:
            return ','.join(self.p0_cards) + self.history[5:]
        else:
            return ','.join(self.p1_cards) + self.history[5:]

    def new_info_set(self) -> InfoSet:
        # Create a new information set object
        return InfoSet(self.info_set_key())


def create_new_history():
    """A function to create an empty history object"""
    return History()
