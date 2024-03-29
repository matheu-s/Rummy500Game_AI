import random
from typing import List, cast, Dict
from random import shuffle
from labml_nn.cfr import History as _History, InfoSet as _InfoSet, Action, Player, CFRConfigs
from engine.mccfr.draw.infoset import InfoSet
from engine.mccfr.rummy_helper import get_possible_melds, calculate_meld_points, sort_hand, is_meld_former, \
    is_hand_melded, get_possible_discard_picks, is_meld, get_card_score, get_game_stage, get_hidden_deck_estimation
from copy import deepcopy

# There are two players
PLAYERS = cast(List[Player], [0, 1])

# Cards in play
CHANCES = cast(List[Action], ['1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '10s', '11s', '12s', '13s',
                              '1d', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', '10d', '11d', '12d', '13d',
                              '1h', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', '11h', '12h', '13h',
                              '1c', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', '10c', '11c', '12c', '13c'])


class History(_History):
    # History
    history = ''
    p0_cards = []
    p1_cards = []
    p0_indiv_points = 0
    p1_indiv_points = 0
    p0_points = 0
    p1_points = 0
    p0_melds = []
    p1_melds = []
    discard_pile = []
    hidden_deck = []
    cpt = {}
    id = 0

    def __init__(self, history: str = '', data: Dict = None):
        """
        Initialize with a given history string
        """

        self.history = history

        if data is not None:
            self.p0_cards = data['p0_cards']
            self.p1_cards = data['p1_cards']
            self.p0_indiv_points = data['p0_indiv_points']
            self.p1_indiv_points = data['p1_indiv_points']
            self.p0_points = data['p0_points']
            self.p1_points = data['p1_points']
            self.p0_melds = data['p0_melds']
            self.p1_melds = data['p1_melds']
            self.discard_pile = data['discard_pile']
            self.hidden_deck = data['hidden_deck']
            self.cpt = data['cpt']
            self.id = data['id'] + 1

    def is_terminal(self):
        """
        Whether the history is terminal (less than 30 moves ahead, after 13 cards dealt).
        """
        # print(self.history)

        if self.history != '':
            # if len(self.hidden_deck) == 0 or len(self.p0_cards) == 0 or len(self.p1_cards) == 0:
            return len(self.hidden_deck) == 0 or len(self.p0_cards) == 0 or len(self.p1_cards) == 0 or self.history[
                                                                                                       -6:] == 'dddddd' or len(self.history) > 16

    def _terminal_utility_p0(self) -> float:
        """
        Calculate the terminal utility for player 0
        """

        self.calculate_points()

        # Discounting gifted points
        self.p0_points += self.p0_indiv_points
        self.p1_points += self.p1_indiv_points

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

        # Draw stage
        if other == 'd':
            self.draw_discard()
        elif other == 'h':
            self.draw_hidden()

        # Melding stage
        self.meld()

        # Discarding stage
        self.discard()

        data = {
            'p0_cards': self.p0_cards,
            'p1_cards': self.p1_cards,
            'p0_indiv_points': self.p0_indiv_points,
            'p1_indiv_points': self.p1_indiv_points,
            'p0_points': self.p0_points,
            'p1_points': self.p1_points,
            'p0_melds': self.p0_melds,
            'p1_melds': self.p1_melds,
            'discard_pile': self.discard_pile,
            'hidden_deck': self.hidden_deck,
            'cpt': self.cpt,
            'id': self.id
        }

        return History(self.history + other, data)

    def draw_discard(self):
        """Draws from discard pile, prioritizing long picks"""

        # Default move is top pick
        move = {
            'card_index': len(self.discard_pile) - 1,
            'mandatory_meld': None
        }

        if self.player() == 0:
            # Get the deepest pick possible
            long_draw = get_possible_discard_picks(self.discard_pile, self.p0_cards)
            if long_draw is not None:
                move = long_draw

            # Removing from discard pile and appending to player's hand
            selected_cards = self.discard_pile[int(move.get('card_index')):]
            picked_cards = selected_cards
            self.discard_pile = self.discard_pile[:int(move.get('card_index'))]
            self.p0_cards += selected_cards

            if move['mandatory_meld'] is not None:
                self.p0_melds.append(move['mandatory_meld'])
                for card in move['mandatory_meld']:
                    self.p0_cards.remove(card)
        else:
            # Get the deepest pick possible
            long_draw = get_possible_discard_picks(self.discard_pile, self.p1_cards)
            if long_draw is not None:
                move = long_draw

            # Removing from discard pile and appending to player's hand
            selected_cards = self.discard_pile[int(move.get('card_index')):]
            picked_cards = selected_cards
            self.discard_pile = self.discard_pile[:int(move.get('card_index'))]
            self.p1_cards += selected_cards

            if move['mandatory_meld'] is not None:
                self.p1_melds.append(move['mandatory_meld'])
                for card in move['mandatory_meld']:
                    self.p1_cards.remove(card)

        # Updating CPT action
        self.cpt.update(
            {
                self.id: {
                    self.player(): {
                        'draw_discard': {
                            # 'cards': ','.join([str(card) for card in picked_cards]),
                            'cards': picked_cards,  # Card = What opp. got
                            'V': -1
                        }
                    }
                }
            }
        )

        # Updating CPT seen cards (engine is capable of keeping track of which cards are in opp. hand after they're
        # drawn from DP)
        already_seen_cards = self.cpt[self.id][self.player()].get('seen_cards')
        if already_seen_cards:
            self.cpt[self.id][self.player()].update({'seen_cards': already_seen_cards + picked_cards})
        else:
            self.cpt[self.id][self.player()].update({'seen_cards': picked_cards})

    def draw_hidden(self):
        card = self.hidden_deck.pop()
        if self.player() == 0:
            self.p0_cards.append(card)
        else:
            self.p1_cards.append(card)

        # Updating CPT
        self.cpt.update(
            {
                self.id: {
                    self.player(): {
                        'draw_hidden': {
                            'cards': [self.discard_pile[-1]],  # Card = What player rejected
                            'V': 1
                        }
                    }
                }
            }
        )

    def meld(self):
        """Forms the highest melds"""

        player = self.player()
        if player == 0:
            hand = self.p0_cards
        else:
            hand = self.p1_cards

        for i in range(17):
            melds = get_possible_melds(sort_hand(hand))

            if len(melds) == 0:
                break

            for meld in melds:
                if player == 0:
                    self.p0_melds.append(meld)
                    for card in meld:
                        if card in hand:
                            hand.remove(card)
                else:
                    self.p1_melds.append(meld)
                    for card in meld:
                        if card in hand:
                            hand.remove(card)
                break

        # Individual lays
        for card in hand:
            is_melded = False
            # Looking for p0 melds
            for meld in self.p0_melds:
                temp_meld = meld
                if is_meld(temp_meld + [card]):
                    is_melded = True
                    meld.append(card)
                    hand.remove(card)
                    break
                if is_meld([card] + temp_meld):
                    is_melded = True
                    meld.insert(0, card)
                    hand.remove(card)
                    break

            # If player 1 melded in p0 melds
            if player == 1 and is_melded:
                self.p1_indiv_points += get_card_score(card)
                self.p0_indiv_points -= get_card_score(card)
                break

            # If player 0 melded in p0 melds... will count in the end the points
            if is_melded:
                break

            # Looking for the p1 melds
            for meld in self.p1_melds:
                if is_meld(meld + [card]):
                    is_melded = True
                    meld.append(card)
                    hand.remove(card)
                    break
                if is_meld([card] + meld):
                    is_melded = True
                    meld.insert(0, card)
                    hand.remove(card)
                    break

            # If player 0 melded in p1 melds
            if player == 0 and is_melded:
                self.p0_indiv_points += get_card_score(card)
                self.p1_indiv_points -= get_card_score(card)
                break

        if player == 0:
            self.p0_cards = hand
        else:
            self.p1_cards = hand

    def discard(self):
        """Discard a card that doesn't form a meld, otherwise random"""

        chosen_card = None
        # Randomly removes a card from hand, if player has any card
        if self.player() == 0 and len(self.p0_cards) != 0:
            chosen_card = random.choice(self.p0_cards)
            self.p0_cards.remove(chosen_card)
        elif self.player() == 1 and len(self.p1_cards) != 0:
            chosen_card = random.choice(self.p1_cards)
            self.p1_cards.remove(chosen_card)

        # Add card to discard pile
        if chosen_card is not None:
            self.discard_pile.append(chosen_card)
            # Updating cpt
            self.cpt[self.id][self.player()].update(
                {
                    'discard': {
                        'cards': [self.discard_pile[-1]],  # Card = What player discard,
                        'V': 1
                    }
                }
            )
            # Removing the card from seen (hand info) after discarded
            already_seen_cards = self.cpt[self.id][self.player()].get('seen_cards')
            if already_seen_cards and self.discard_pile[-1] in already_seen_cards:
                self.cpt[self.id][self.player()].update(
                    {'seen_cards': already_seen_cards.remove(self.discard_pile[-1])})

    def calculate_points(self):
        """Calculates points of best melds in hand, set self points"""

        # Summing meld points
        for meld in self.p0_melds:
            self.p0_points += calculate_meld_points(meld)
        for meld in self.p1_melds:
            self.p1_points += calculate_meld_points(meld)

        # Reducing points from cards in hand
        for card in self.p0_cards:
            self.p0_points -= get_card_score(card)
        for card in self.p1_cards:
            self.p1_points -= get_card_score(card)

    def player(self) -> Player:
        """
        Current player
        """
        return cast(Player, len(self.history) % 2)

    def sample_chance(self) -> Action:
        """
        Deal cards
        """

        # Restarting game properties
        self.p0_cards = []
        self.p1_cards = []
        self.discard_pile = []
        self.hidden_deck = []
        self.p0_melds = []
        self.p1_melds = []
        self.cpt = {}

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

        # Restarting points
        self.p0_points = 0
        self.p1_points = 0

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
        # Current player sees his card and the actions
        if self.player() == 0:
            # 4 danger - 3 late - 2 mid - 1 early
            game_stage = get_game_stage(len(self.hidden_deck), len(self.p0_cards), len(self.p1_cards))

            # 3 forms meld - 2 forms pair - 1 none
            top_card_discard_is_meldable = is_meld_former(self.discard_pile[-1], self.p0_cards)

            # bayesian layer estimation of deck utility
            visible_data = {
                'p0_cards': self.p0_cards,
                'p0_melds': self.p0_melds,
                'discard_pile': self.discard_pile,
                'p1_melds': self.p1_melds
            }
            deck_utility_estimation = get_hidden_deck_estimation(self.cpt, 0, visible_data, len(self.hidden_deck))

            # print('returning stage ', game_stage , ' for IS')
            return f'{game_stage}-{top_card_discard_is_meldable}-{deck_utility_estimation}'
        else:
            # Stage of the game (4 - danger - 3 late - 2 mid - 1 early)
            game_stage = get_game_stage(len(self.hidden_deck), len(self.p1_cards), len(self.p0_cards))

            # Discard pile pick outcome (3 forms meld - 2 forms pair - 1 none)
            top_card_discard_is_meldable = is_meld_former(self.discard_pile[-1], self.p1_cards)

            # Hidden deck utility (3 - high, 2 - mid, 1 - low)
            visible_data = {
                'p1_cards': self.p1_cards,
                'p1_melds': self.p1_melds,
                'discard_pile': self.discard_pile,
                'p0_melds': self.p0_melds
            }
            deck_utility_estimation = get_hidden_deck_estimation(self.cpt, 1, visible_data, len(self.hidden_deck))

            return f'{game_stage}-{top_card_discard_is_meldable}-{deck_utility_estimation}'

    def new_info_set(self) -> InfoSet:
        # Create a new information set object
        return InfoSet(self.info_set_key())


def create_new_history():
    """A function to create an empty history object"""
    return History()
