from game.card import Card


class Hand:
    cards = None
    pos = None

    def __init__(self, cards):
        self.cards = cards
        self.pos = 0

    def sort(self):
        cards_dict = {
            'spades': [],
            'hearts': [],
            'clubs': [],
            'diamonds': [],
            'joker_red': [],
            'joker_black': []
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
