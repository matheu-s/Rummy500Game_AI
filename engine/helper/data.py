from itertools import combinations
from engine.helper.node import Node


class Data:
    p0_cards = None
    p1_cards = None
    p1_cards_len = None
    p0_points = None
    p1_points = None
    p0_melds = None
    p1_melds = None
    deck_cards = None
    discard_pile_cards = None
    root = None

    def set_board_data(self, data):
        """" Updates class data\""""

        self.p0_cards = data['p0_cards']
        self.p1_cards = data['p1_cards']
        self.p1_cards_len = data['p1_hand_length']
        self.p0_points = data['p0_points']
        self.p1_points = data['p1_points']
        self.p0_melds = data['p0_melds']
        self.p1_melds = data['p1_melds']
        self.deck_cards = data['deck_cards']
        self.discard_pile_cards = data['discard_pile_cards']
        self.root = Node(data, 0)

    def generate_game_tree(self, depth=3):
        print('generating partial tree')

    def get_possible_melds(self, hand=None):
        """" Get all possible melds in p0 hand\""""

        if hand is None:
            hand = self.p0_cards

        melds = []
        # Checking possible sequences and groups
        for r in range(3, len(hand) + 1):
            for comb in combinations(hand, r):
                comb = list(comb)
                if self.is_meld(comb):
                    melds.append(comb)

        return melds

    def is_seq(self, cards):
        for ind in range(1, len(cards)):
            if cards[ind - 1][-1:] != cards[ind][-1:]:
                return False
            if int(cards[ind - 1][:-1]) != int(cards[ind][:-1]) - 1:
                return False
        return True

    def is_group(self, cards):
        for ind in range(1, len(cards)):
            if cards[ind - 1][:-1] != cards[ind][:-1]:
                return False
        return True


    def is_meld(self, cards):
        """" Checks if provided combination is a meld \""""

        return self.is_seq(cards) or self.is_group(cards)

    def get_possible_lays(self, hand=None):
        """" Checks possible individuals cards to lay into existing melds \""""

        if not hand:
            hand = self.p0_cards

        melds = {
            'p0': {},
            'p1': {}
        }
        for card in hand:
            melded = False
            for e_meld in self.p0_melds:
                if self.is_meld(card + e_meld) or self.is_meld(e_meld + card):
                    melds['p0_melds'][card] = e_meld
                    melded = True
                    break

            if melded:
                continue

            for e_meld in self.p1_melds:
                if self.is_meld(card + e_meld) or self.is_meld(e_meld + card):
                    melds['p1_melds'][card] = e_meld
                    break

        return melds

    def get_possible_discard_picks(self, discard_pile_cards=None, hand=None):
        """" Checks possible picks from discard pile, returns a list of dicts with index and mandatory melds \""""

        if not discard_pile_cards:
            discard_pile_cards = self.discard_pile_cards
        if not hand:
            hand = self.p0_cards

        possible_picks = []

        picked = False
        for index in range(len(discard_pile_cards)):
            temp_hand = self.sort_hand(hand + discard_pile_cards[index:])
            # print('picked: ', discard_pile_cards[index:])
            # print('temp hand: ', temp_hand)
            melds = self.get_possible_melds(temp_hand)
            # print('formed melds: ', melds)

            for meld in melds:
                if discard_pile_cards[index] in meld:
                    # print('picked card forms meld: ', discard_pile_cards[index], ' on ', meld)
                    # Saving the meld that must be layed, according to rules
                    possible_picks.append({
                        'card_index': index,
                        'mandatory_meld': meld
                    })
                    picked = True
                    break

            # Breaking as soon as first pick is found (optional)
            if picked:
                break

        # print('returning picks.. ', possible_picks)
        return possible_picks


    def is_discard_pick_worth(self):
        """" Evaluates if picking from discard is ok \""""

        # TODO: Evaluates if picking from discard is ok, myb simulate if points worth for next 3 levels... usually yes
        # combine with BN to check if there isn't few cards in deck.. ?

    def calculate_meld_points(self, meld):
        """" Calculates points of a meld combination \""""

        points = 0
        for card in meld:
            if int(card[:-1]) > 10:
                points += 10
                continue
            points += 5

        return points

    def get_pairs(self, hand=None):
        """" Gets all pairs\""""

        if hand is None:
            hand = self.p0_cards

        pairs = []
        # Checking possible sequences and groups
        for pair in combinations(hand, 2):
            pair = list(pair)
            if self.is_meld(pair):
                pairs.append(pair)

        return pairs

    def get_lowest_card(self, hand=None):
        """" Gets the lowest value card, if more than one, return any between them\""""

        if hand is None:
            hand = self.p0_cards

        lowest_card = None
        lowest_value = 14
        for card in hand:
            if int(card[:-1]) < lowest_value:
                lowest_value = int(card[:-1])
                lowest_card = card

        return lowest_card

    def sort_hand(self, hand):
        """" Returns the hand sorted\""""

        cards_dict = {
            's': [],
            'h': [],
            'c': [],
            'd': []
        }

        for i in hand:
            cards_dict[i[-1:]].append(int(i[:-1]))

        cards_dict['s'].sort()
        cards_dict['h'].sort()
        cards_dict['c'].sort()
        cards_dict['d'].sort()

        sorted_cards = []
        for suit in cards_dict:
            for i in cards_dict[suit]:
                sorted_cards.append(str(i)+suit)

        return sorted_cards







