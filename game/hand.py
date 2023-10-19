from itertools import combinations
from game.card import Card
from game.meld import Meld


class Hand:
    cards = None
    pos = None

    def __init__(self, cards=None):
        self.cards = cards
        self.pos = 0

    def set_cards(self, cards):
        self.cards = cards

    def add_cards(self, cards):
        if type(cards) == list:
            for i in cards:
                self.cards.append(i)
                self.pos += 25
        else:
            self.cards.append(cards)
            self.pos += 25

    def discard(self, card):
        self.cards.remove(card)
        self.pos -= 25

    def sort(self):
        cards_dict = {
            's': [],
            'h': [],
            'c': [],
            'd': []
        }

        for i in self.cards:
            cards_dict[i.suit].append(int(i.value))

        cards_dict['s'].sort()
        cards_dict['h'].sort()
        cards_dict['c'].sort()
        cards_dict['d'].sort()

        self.cards = []
        for suit in cards_dict:
            values = cards_dict[suit]
            for i in values:
                self.cards.append(Card(i, suit))

        return self.cards

    def get_melds(self):
        # Saving current hand order and sorting to check melds
        self.sort()

        sequences = []
        groups = []
        # Checking possible sequences and groups
        for r in range(3, len(self.cards) + 1):
            for comb in combinations(self.cards, r):
                comb = list(comb)
                if self.is_meld(comb):
                    sequences.append(comb)

        return sequences, groups

    def meld(self, meld):
        for card in meld.cards:
            for own_card in self.cards:
                if card.suit == own_card.suit and card.value == own_card.value:
                    self.cards.remove(own_card)
                    self.pos -= 25

    def is_meld(self, cards):
        def is_seq(cards2):
            for ind in range(1, len(cards2)):
                if cards2[ind - 1].suit != cards2[ind].suit:
                    return False
                if cards2[ind - 1].value != cards2[ind].value - 1:
                    return False
            return True

        def is_group(cards2):
            for ind in range(1, len(cards2)):
                if cards2[ind - 1].value != cards2[ind].value:
                    return False
            return True

        return is_seq(cards) or is_group(cards)
