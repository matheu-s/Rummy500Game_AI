import pygame
from game.components.hand import Hand


class Player:
    name = None
    hand = None
    melds = []
    points = None
    indiv_points = None

    def __init__(self, is_human):
        self.is_human = is_human
        self.hand = Hand()
        self.melds = []
        self.points = 0
        self.indiv_points = 0 # Points from individual laid cards

    def set_hand(self, hand):
        self.hand = hand

    def get_points(self):
        self.points = 0
        for meld in self.melds:
            self.points += meld.calculate_points()
        self.points += self.indiv_points
        return self.points

    def add_indiv_points(self, card_value):
        card_value = int(card_value)
        if card_value > 10:
            card_value = 10
        else:
            card_value = 5
        self.indiv_points += card_value

