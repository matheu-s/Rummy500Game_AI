from itertools import combinations
from engine.helper.node import Node


class Data:
    board_data = None
    root = None

    def set_board_data(self, data):
        """" Updates class data\""""

        self.board_data = data
        self.root = Node(data)

    def generate_game_tree(self):
        print('generating partial tree')

    def get_possible_melds(self):
        """" Get all possible melds in engine hand\""""

        sequences = []
        groups = []
        # Checking possible sequences and groups
        for r in range(3, len(self.board_data['engine_cards']) + 1):
            for comb in combinations(self.board_data['engine_cards'], r):
                comb = list(comb)
                if self.is_meld(comb):
                    sequences.append(comb)

        return sequences, groups

    def is_meld(self, cards):
        """" Checks is provided combination is a meld \""""

        def is_seq(cards2):
            for ind in range(1, len(cards2)):
                if cards2[ind - 1][-1:] != cards2[ind][-1:]:
                    return False
                if int(cards2[ind - 1][:-1]) != int(cards2[ind][:-1]) - 1:
                    return False
            return True

        def is_group(cards2):
            for ind in range(1, len(cards2)):
                if cards2[ind - 1][:-1] != cards2[ind][:-1]:
                    return False
            return True

        return is_seq(cards) or is_group(cards)

    def get_possible_lays(self):
        """" Checks possible individuals cards to lay into existing melds \""""

        melds = {
            'engine': {},
            'human': {}
        }
        for card in self.board_data['engine_cards']:
            melded = False
            for e_meld in self.board_data['engine_melds']:
                if self.is_meld(card + e_meld) or self.is_meld(e_meld + card):
                    melds['engine_melds'][card] = e_meld
                    melded = True
                    break

            if melded:
                continue

            for e_meld in self.board_data['human_melds']:
                if self.is_meld(card + e_meld) or self.is_meld(e_meld + card):
                    melds['human_melds'][card] = e_meld
                    break

        return melds

