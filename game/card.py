import pygame


class Card:
    value = None
    suit = None
    image = None
    rect = None
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.image = pygame.image.load(f'assets/images/cards/{value}_{suit}.png')
        self.rect = None

    def set_rect(self, rect):
        # Changes width to 25 to make only 1 clickable in the hand
        left, top, width, height = rect
        self.rect = pygame.Rect(left, top, 25, height)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

