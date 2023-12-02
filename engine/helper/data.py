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

        if hand is None:
            hand = self.engine_cards

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
        """" Checks possible picks from discard pile, returns a list of dicts with index and mandatory melds \""""

        if not discard_pile_cards:
            discard_pile_cards = self.discard_pile_cards
        if not hand:
            hand = self.engine_cards

        possible_picks = []

        picked = False
        for index in range(len(discard_pile_cards)):
            temp_hand = self.sort_hand(hand + discard_pile_cards[index:])
            print('picked: ', discard_pile_cards[index:])
            print('temp hand: ', temp_hand)
            melds = self.get_possible_melds(temp_hand)
            print('formed melds: ', melds)

            for meld in melds:
                if discard_pile_cards[index] in meld:
                    print('picked card forms meld: ', discard_pile_cards[index], ' on ', meld)
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

        print('returning picks.. ', possible_picks)
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
            hand = self.engine_cards

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
            hand = self.engine_cards

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







