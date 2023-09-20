import random
from itertools import combinations
from config.constants import *
from game.card import Card


class Deck:
    cards = None

    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for value in range(1, 14):
                self.cards.append(Card(value, suit))
        self.cards.append(Card(0, 'joker_black'))
        self.cards.append(Card(0, 'joker_red'))

    def shuffle(self):
        random.shuffle(self.cards)

    def length(self):
        return len(self.cards)

    def deal(self, number_of_cards=1):
        dealt = self.cards[-number_of_cards:]
        self.cards = self.cards[:-number_of_cards]
        return dealt

