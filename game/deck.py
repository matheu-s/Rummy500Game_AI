import random
from random import shuffle
from config.constants import *
from card import Card


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
