from engine.helper.data import Data
from config.constants import Actions


# Simple Rummy Player
class SimpleRP:
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

    def get_draw_move(self):
        """" Evaluates and chooses where to pick the card from\""""

        # Preference for discard pile, the deepest possible, otherwise... from hidden
        possible_discard_picks = self.data_helper.get_possible_discard_picks()
        if len(possible_discard_picks):
            self.move['action'] = Actions.DRAW_DISCARD.value
            self.move['target'] = possible_discard_picks[0]
            return self.move

        self.move['action'] = Actions.DRAW_HIDDEN.value
        return self.move

    def get_discard_move(self):
        """" Always discard the lowest card \""""

        self.move['action'] = Actions.DISCARD.value
        self.move['target'] = self.data_helper.p0_cards[0]
        return self.move

    def get_meld_combinations_move(self):
        """" Generates, evaluates and chooses the melds\""""

        dict_meld = {
            'group': [],
            'seq': []
        }
        seqs, groups = self.data_helper.get_possible_melds()
        if not len(seqs) and not len(groups):
            return []
        if len(groups):
            dict_meld['group'] = [groups[0]]
        if len(seqs):
            dict_meld['seq'] = [seqs[0]]

        print('returned: ', dict_meld)
        return dict_meld

    def get_individual_lays(self):
        """" Chooses individual card lays into existing melds\""""

        # Always laying all possible cards
        return self.data_helper.get_possible_lays()
