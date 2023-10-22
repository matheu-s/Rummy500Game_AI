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

        # print('in node.. my state is: ')
        # print(self.state)




