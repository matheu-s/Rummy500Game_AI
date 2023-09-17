import pygame


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.image = pygame.image.load(f'assets/images/cards/{value}_of_{suit}.png')

    def render(self):
        return True
