class Node:
    state = None
    player = None
    ancestor = None
    descendants = None

    def __init__(self, state, player=None, ancestor=None):
        self.state = state
        self.player = player
        self.ancestor = ancestor
        self.descendants = []

    def is_terminal(self):
        if len(self.state['p0_cards']) == 0 \
                or len(self.state['p1_cards']) == 0 \
                or len(self.state['deck_cards']) == 0 \
                or self.state['p1_points'] > 499 \
                or self.state['p0_points'] > 499:
            return True
        return False





