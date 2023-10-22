from engine.helper.data import Data
from config.constants import Actions


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

        # Draw from hidden or discard pile
        # self.move['action'] = 'draw_hidden'
        # self.move['target'] = ''
        self.move['action'] = Actions.DRAW_DISCARD.value
        self.move['target'] = 0
        return self.move

    def get_discard_move(self):
        """" Evaluates and choose the card to discard\""""

        # TODO: Add logic to discard action
        self.move['action'] = Actions.DISCARD.value
        self.move['target'] = self.data_helper.board_data['engine_cards'][0]
        return self.move

    def get_meld_combinations_move(self):
        """" Generates, evaluates and chooses the melds\""""

        dict_meld = {
            'group': [],
            'seq': []
        }
        seqs, groups = self.data_helper.get_possible_melds()
        if not len(seqs) and not len(groups):
            print('no melds')
            return []
        if len(groups):
            dict_meld['group'] = [groups[0]] # TODO: remove [0]
        if len(seqs):
            dict_meld['seq'] = [seqs[0]] # TODO: remove [0]
        # TODO: Evaluate and select best melds...
        print('returned: ', dict_meld)
        return dict_meld

    def get_individual_lays(self):
        """" Chooses individual card lays into existing melds\""""

        # Until the moment, simply laying cards, preferring own melds. No further evaluation as changes are minors
        return self.data_helper.get_possible_lays()








