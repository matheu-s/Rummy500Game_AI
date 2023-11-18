from engine.helper.data import Data
from config.constants import Actions


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

    def get_the_best_move(self):
        self.data_helper.generate_game_tree()
        # getting move...
        self.move['action'] = 'draw_hidden'
        return self.move

    def get_draw_move(self):
        """" Evaluates and chooses where to pick the card from\""""

        # Preference for discard pile, the deepest possible, otherwise... from hidden
        possible_discard_picks = self.data_helper.get_possible_discard_picks()
        if len(possible_discard_picks):
            print('getting from discard pile,')
            self.move['action'] = Actions.DRAW_DISCARD.value
            self.move['target'] = possible_discard_picks[0]
            return self.move

        self.move['action'] = Actions.DRAW_HIDDEN.value
        return self.move

    def get_discard_move(self):
        """" Evaluates and choose the card to discard\""""

        # TODO: Add logic to discard action
        self.move['action'] = Actions.DISCARD.value
        self.move['target'] = self.data_helper.engine_cards[0]
        return self.move

    def get_meld_combinations_move(self):
        """" Generates, evaluates and chooses the melds\""""

        dict_meld = {
            'melds': []
        }

        hand = self.data_helper.engine_cards

        # Iterate until all melds are filtered
        while len(self.data_helper.get_possible_melds(hand)) != 0:
            melds = self.data_helper.get_possible_melds(hand)

            # Getting the highest pointing meld and removing cards for next iteration
            highest_score = 0
            for meld in melds:
                if self.data_helper.calculate_meld_points(meld) > highest_score:
                    dict_meld['melds'].append(meld)
                    for card in meld:
                        hand.remove(card)

        return dict_meld

    def get_individual_lays(self):
        """" Chooses individual card lays into existing melds\""""

        # Until the moment, simply laying cards, preferring own melds. No further evaluation as changes are minors
        return self.data_helper.get_possible_lays()
