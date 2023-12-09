from engine.helper.data import Data
from config.constants import Actions
import random
from itertools import chain


# Souza's Rummy Solver
class SRS:
    data_helper = None
    move = None

    def __init__(self):
        self.data_helper = Data()
        self.move = {
            'action': Actions,
            'target': 0,
        }

    def update_data(self, data):
        """" Updates Helper class data\""""

        self.data_helper.set_board_data(data)
        print('engine cards: ', self.data_helper.p0_cards)

    def get_draw_move(self):
        """" Evaluates and chooses where to pick the card from\""""

        # Preference for discard pile, the deepest possible, otherwise... from hidden
        possible_discard_picks = self.data_helper.get_possible_discard_picks()
        if len(possible_discard_picks):
            pick = possible_discard_picks[0] # Getting the deepest pick
            self.move['action'] = Actions.DRAW_DISCARD.value
            self.move['target'] = pick
            return self.move

        self.move['action'] = Actions.DRAW_HIDDEN.value
        return self.move

    def get_discard_move(self, player=0):
        """" Evaluates and choose the card to discard\""""

        if player == 1:
            hand = self.data_helper.p1_cards
        else:
            hand = self.data_helper.p0_cards

        # Avoiding to discard pairs
        not_almost_meld_cards = []
        pairs = self.data_helper.get_pairs(hand)
        cards = list(chain.from_iterable(pairs))
        set_cards = set(cards)
        for card in hand:
            if card in set_cards:
                continue
            not_almost_meld_cards.append(card)

        print('hand ', hand)
        if not len(not_almost_meld_cards):
            # If all cards have pairs, discard random
            self.move['target'] = random.choice(hand)
            print('yep ', self.move['target'])
        else:
            # If more than one not-pair, discard random between them
            self.move['target'] = random.choice(not_almost_meld_cards)

        self.move['action'] = Actions.DISCARD.value

        return self.move

    def get_meld_combinations_move(self):
        """" Generates, evaluates and chooses the melds\""""

        dict_meld = {
            'melds': []
        }

        hand = self.data_helper.sort_hand(self.data_helper.p0_cards)
        # print('checking melds from: ', hand)

        # Iterate until all melds are filtered
        while len(self.data_helper.get_possible_melds(hand)) != 0:
            melds = self.data_helper.get_possible_melds(hand)

            # Getting the highest pointing meld and removing cards for next iteration
            highest_score = 0
            highest_meld = None
            for meld in melds:
                if self.data_helper.calculate_meld_points(meld) > highest_score:
                    highest_meld = meld

            if highest_meld is not None:
                dict_meld['melds'].append(highest_meld)
                for card in highest_meld:
                    hand.remove(card)

        return dict_meld

    def get_individual_lays(self):
        """" Chooses individual card lays into existing melds\""""

        # Until the moment, simply laying cards, preferring own melds. No further evaluation as changes are minors
        return self.data_helper.get_possible_lays()
