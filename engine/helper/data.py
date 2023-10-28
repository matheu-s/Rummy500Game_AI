from itertools import combinations
from engine.helper.node import Node


class Data:
    engine_cards = None
    human_cards_len = None
    engine_points = None
    human_points = None
    engine_melds = None
    human_melds = None
    discard_pile_cards = None
    all_cards = None
    seen_cards = None
    unseen_cards = None
    root = None

    def set_board_data(self, data):
        """" Updates class data\""""

        self.engine_cards = data['engine_cards']
        self.human_cards_len = data['human_hand_length']
        self.engine_points = data['engine_points']
        self.human_points = data['human_points']
        self.engine_melds = data['engine_melds']
        self.human_melds = data['human_melds']
        self.discard_pile_cards = data['discard_pile_cards']
        self.all_cards = data['all_cards']
        self.seen_cards = data['seen_cards']
        self.unseen_cards = data['unseen_cards']
        self.root = Node(data)

    def generate_game_tree(self, depth=3):
        print('generating partial tree')

    def get_possible_melds(self, hand=None):
        """" Get all possible melds in engine hand\""""

        if not hand:
            hand = self.engine_cards
        sequences = []
        groups = []
        # Checking possible sequences and groups
        for r in range(3, len(hand) + 1):
            for comb in combinations(hand, r):
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

    def get_possible_lays(self, hand=None):
        """" Checks possible individuals cards to lay into existing melds \""""

        if not hand:
            hand = self.engine_cards

        melds = {
            'engine': {},
            'human': {}
        }
        for card in hand:
            melded = False
            for e_meld in self.engine_melds:
                if self.is_meld(card + e_meld) or self.is_meld(e_meld + card):
                    melds['engine_melds'][card] = e_meld
                    melded = True
                    break

            if melded:
                continue

            for e_meld in self.human_melds:
                if self.is_meld(card + e_meld) or self.is_meld(e_meld + card):
                    melds['human_melds'][card] = e_meld
                    break

        return melds

    def get_possible_discard_picks(self, discard_pile_cards=None, hand=None):
        """" Checks possible picks from discard pile, returns indexes of possible cards \""""

        if not discard_pile_cards:
            discard_pile_cards = self.discard_pile_cards
        if not hand:
            hand = self.engine_cards

        possible_picks = []

        picked = False
        for index in range(len(discard_pile_cards)):
            temp_hand = hand + discard_pile_cards[index-1:]
            seqs, groups = self.get_possible_melds(temp_hand)
            melds = seqs+groups

            for meld in melds:
                if discard_pile_cards[index-1] in meld:
                    possible_picks.append(index-1)
                    picked = True
                    break
            if picked:
                break

        return possible_picks


    def is_discard_pick_worth(self):
        """" Evaluates if picking from discard is ok \""""

        # TODO: Evaluates if picking from discard is ok, myb simulate if points worth for next 3 levels... usually yes
        # combine with BN to check if there isn't few cards in deck.. ?



