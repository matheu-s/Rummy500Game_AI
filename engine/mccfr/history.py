from labml_nn.cfr import History as _History
from engine.mccfr.infoset import InfoSet, Player, Action, ACTIONS, PLAYERS
from typing import cast, List
from engine.helper.game import Game

game = Game()
new_data = game.get_new_game()


# SIMPLE FOR NOW
# GET HIDDEN OR TOP OF DISCARD PILE
# later implement training of checking all possible discard picks... and game length
class History(_History):
    history: {}

    def __init__(self, history: {} = None):
        if history is None:
            # Creating new initial game state
            history_new = {
                'key': ','.join(new_data['p0_cards']) + '-' + ','.join(new_data['discard_pile_cards']),
                'collection': [[game.data]],
                'player': 0
            }
            self.history = history_new
        else:
            self.history = history

    def is_root(self):
        return len(self.history['collection']) == 1

    def is_terminal(self):
        return game.is_terminal(self.history['collection'][-1][0])

    def terminal_utility(self, i: Player) -> float:
        # If player 0
        if i == PLAYERS[0]:
            return self._terminal_utility_p1()

        # if player 1, invert
        return -1 * self._terminal_utility_p1()

    def _terminal_utility_p1(self) -> float:
        """Returns the points difference if p1 is ahead, otherwise 0"""

        return self.history['collection'][-1][0]['p0_points'] - self.history['collection'][-1][0]['p1_points']

    def player(self) -> Player:
        """Returns current player of the History"""

        return self.history['player']

    def __add__(self, action: Action):
        self.collection.append()

    def draw_from_discard(self):
        next_state = game.draw_discard()

        history = {
            'key': self.history['key'],
            'collection': self.history['collection'] + [[next_state]],
            'player': game.player
        }

        return History(history)

    def draw_from_hidden(self):

        # print('current: ', self.history)
        next_state = game.draw_hidden()
        # print('next: ', next_state)

        history = {
            'key': self.history['key'],
            'collection': self.history['collection'] + [[next_state]],
            'player': game.player
        }

        return History(history)

    def info_set_key(self) -> str:
        return self.history['key']

    def new_info_set(self) -> 'InfoSet':
        return InfoSet(self.info_set_key())

    def __repr__(self):
        return repr(self.history['key'])

