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

