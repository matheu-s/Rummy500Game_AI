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
        self.data_helper.set_board_data(data)

    def get_the_best_move(self):
        self.data_helper.generate_game_tree()
        # getting move...
        self.move['action'] = 'draw_hidden'
        return self.move

    def get_draw_move(self):
        # Draw from hidden or discard pile
        # self.move['action'] = 'draw_hidden'
        # self.move['target'] = ''
        self.move['action'] = Actions.DRAW_DISCARD.value
        self.move['target'] = 0
        return self.move

    def get_discard_move(self):
        # Choose which card to discard

        index_card = 5
        self.move['action'] = Actions.DISCARD.value
        self.move['target'] = index_card

    def get_meld_combinations_move(self):
        seqs, groups = self.data_helper.get_possible_melds()
        print('ENGINE CARDS: ', self.data_helper.board_data['engine_cards'])
        print('melds: ', seqs, groups)

