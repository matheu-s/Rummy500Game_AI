from game.card import Card


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
        else:
            self.cards.append(card)

    def get_card(self, card, index=0):
        # Returns the chosen card and all cards on top of it
        selected_cards = self.cards[index:]
        self.cards = self.cards[:index]

        return selected_cards






