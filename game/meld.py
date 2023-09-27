import pygame
from game.card import Card


class Meld:
    cards = None
    points = None

    def __init__(self, cards):
        self.cards = cards
        self.points = 0

    def calculate_points(self):
        # TODO
        print('calculate points')

    def is_clicked(self, mouse_pos):
        for card in self.cards:
            if card.is_clicked(mouse_pos):
                return True
        return False

