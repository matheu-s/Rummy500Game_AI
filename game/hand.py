from itertools import combinations
from game.card import Card


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
            'spades': [],
            'hearts': [],
            'clubs': [],
            'diamonds': []
        }

        for i in self.cards:
            cards_dict[i.suit].append(int(i.value))

        cards_dict['spades'].sort()
        cards_dict['hearts'].sort()
        cards_dict['clubs'].sort()
        cards_dict['diamonds'].sort()

        self.cards = []
        for suit in cards_dict:
            values = cards_dict[suit]
            for i in values:
                self.cards.append(Card(i, suit))

        return self.cards

    def get_melds(self):
        # Saving current hand order and sorting to check melds
        copy_cards = self.cards
        self.sort()

        sequences = []
        groups = []

        def is_seq(cards):
            for ind in range(1, len(cards)):
                if cards[ind - 1].suit != cards[ind].suit:
                    return False
                if cards[ind - 1].value != cards[ind].value - 1:
                    return False
            return True

        def is_group(cards):
            for ind in range(1, len(cards)):
                if cards[ind - 1].value != cards[ind].value:
                    return False
            return True

        # Checking possible sequences and groups
        for r in range(3, len(self.cards) + 1):
            for comb in combinations(self.cards, r):
                comb = list(comb)
                if is_seq(comb):
                    sequences.append(comb)
                elif is_group(comb):
                    groups.append(comb)

        self.cards = copy_cards
        return sequences, groups

    def meld(self, meld):
        for card in meld.cards:
            for own_card in self.cards:
                if card.suit == own_card.suit and card.value == own_card.value:
                    self.cards.remove(own_card)
                    self.pos -= 25

