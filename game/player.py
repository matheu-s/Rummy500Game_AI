import pygame
from game.hand import Hand


class Player:
    name = None
    hand = None
    melds = []
    points = None

    def __init__(self, is_human):
        self.is_human = is_human
        self.hand = Hand()
        self.melds = []
        self.points = 0

    def set_hand(self, hand):
        self.hand = hand

    def get_points(self):
        self.points = 0
        for meld in self.melds:
            self.points += meld.calculate_points()
        return self.points

