from engine.helper.node import Node


class Data:
    board_data = None
    root = None

    def set_board_data(self, data):
        self.board_data = data
        self.root = Node(data)

    def generate_game_tree(self):
        print('generating partial tree')
