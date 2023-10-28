from game.components.card import Card


class DiscardPile:
    cards = None
    pos = None

    def __init__(self):
        self.cards = []
        self.pos = 0

    def add_card(self, card):
        if type(card) == list:
            for i in card:
                self.cards.append(i)
                self.pos += 25
        else:
            self.cards.append(card)
            self.pos += 25

    def get_card(self, index):
        # Returns the chosen card and all cards on top of it

        selected_cards = self.cards[index:]
        self.cards = self.cards[:index]
        self.pos = 25 * len(self.cards)
        return selected_cards






