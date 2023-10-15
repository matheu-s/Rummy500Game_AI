from engine.helper.data import Data


class SRS:
    data_helper = None
    move = None

    def __init__(self):
        self.data_helper = Data()
        self.move = {
            'action': '',
            'target': '',
            }

    def update_data(self, data):
        self.data_helper.set_board_data(data)

    def get_the_best_move(self):
        self.data_helper.generate_game_tree()
        # getting move...
        self.move['action'] = 'draw_hidden'
        return self.move

    def get_draw_action(self):
        return 'draw_hidden'
