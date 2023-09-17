import pygame, time, os, sys
from config.constants import *


class Board:
    def __init__(self):
        self.human_cards = []
        self.engine_cards = []
        self.cards = {
            '1,1': pygame.rect, '1,2': pygame.rect, '1,3': pygame.rect, '1,4': pygame.rect,
            '2,1': pygame.rect, '2,2': pygame.rect, '2,3': pygame.rect, '2,4': pygame.rect,
            '3,1': pygame.rect, '3,2': pygame.rect, '3,3': pygame.rect, '3,4': pygame.rect,
            '4,1': pygame.rect, '4,2': pygame.rect, '4,3': pygame.rect, '4,4': pygame.rect,
        }

    def start_board(self, screen):
        # Inserting hidden deck
        hidden_deck = pygame.image.load(f'assets/images/cards/back_side.png')
        hidden_deck_width = 686 * 0.15
        hidden_deck_heigth = 976 * 0.15
        hidden_deck = pygame.transform.scale(hidden_deck, (int(hidden_deck_width), int(hidden_deck_heigth)))
        screen.blit(hidden_deck, (400, (HEIGHT/2) - (hidden_deck_heigth/2)))


        pygame.display.update()

    # def deal(self):
