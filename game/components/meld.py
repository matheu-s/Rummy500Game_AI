import pygame
from game.components.card import Card


class Meld:
    cards = None
    type = None
    points = None
    points_added = None

    def __init__(self, cards, meld_type):
        self.cards = cards
        self.meld_type = meld_type
        self.points = 0
        self.points_decrease = 0

    def calculate_points(self):
        """" Returns the points of the meld\""""

        self.points = 0
        for card in self.cards:
            self.points += card.points
        return self.points - self.points_decrease

    def is_clicked(self, mouse_pos):
        """" Checks if any card from this meld was clicked\""""

        for card in self.cards:
            if card.is_clicked(mouse_pos):
                return True
        return False

    def add_card(self, card, points_dec=None):
        """" Adds individual cards\""""

        # Subtracting points when card added by opponent
        if points_dec:
            points_dec = int(points_dec)
            if points_dec > 10:
                points_dec = 10
            else:
                points_dec = 5
            self.points_decrease += points_dec

        # Just append anywhere if it's group
        if self.type == 'group':
            self.cards.append(card)
            return

        # Check if it goes in beginning or end
        if self.cards[0].value == card.value + 1:
            self.cards.insert(0, card)
            return
        self.cards.append(card)



