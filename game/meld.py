import pygame
from game.card import Card


class Meld:
    cards = None
    type = None
    points = None

    def __init__(self, cards, meld_type):
        self.cards = cards
        self.meld_type = meld_type
        self.points = 0

    def calculate_points(self):
        self.points = 0
        for card in self.cards:
            self.points += card.points
        return self.points

    def is_clicked(self, mouse_pos):
        for card in self.cards:
            if card.is_clicked(mouse_pos):
                return True
        return False

    def add_card(self, card):
        # Just append anywhere if it's group
        if self.type == 'group':
            self.cards.append(card)
            return

        # Check if it goes in beginning or end
        if self.cards[0].value == card.value + 1:
            self.cards.insert(0, card)
            return
        self.cards.append(card)



