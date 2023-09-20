import pygame, time, os, sys
from config.constants import *
from game.deck import Deck


class Board:
    hidden_deck_rect = None
    pile = None
    human_cards = None
    engine_cards = None
    def __init__(self):
        self.hidden_deck_rect = None
        self.pile = []
        self.human_cards = []
        self.engine_cards = []


    def start_board(self, screen):
        # Inserting hidden deck
        hidden_deck = pygame.image.load(f'assets/images/cards/back_side.png')
        hidden_deck_width = 686 * 0.15
        hidden_deck_heigth = 976 * 0.15
        hidden_deck = pygame.transform.scale(hidden_deck, (int(hidden_deck_width), int(hidden_deck_heigth)))
        self.hidden_deck_rect = screen.blit(hidden_deck, (650, (HEIGHT/2) - (hidden_deck_heigth/2)))

        deck = Deck()
        deck.shuffle()

        self.human_cards = deck.deal(13)
        self.engine_cards = deck.deal(13)
        self.pile = deck.deal()

        card_width = 500 * 0.204
        card_height = 726 * 0.204

        counter = 0
        for i in self.human_cards:
            card = pygame.transform.scale(i.image, (int(card_width), int(card_height)))
            screen.blit(card, (600+counter, (HEIGHT) - (card_height + 20)))
            counter += 25

        counter = 0
        hidden_img = pygame.image.load(f'assets/images/cards/back_side.png')
        for i in self.engine_cards:
            card = pygame.transform.scale(hidden_img, (int(card_width), int(card_height)))
            screen.blit(card, (600+counter, 20))
            counter += 25

        for i in self.pile:
            card = pygame.transform.scale(i.image, (int(card_width), int(card_height)))
            counter += 25
            screen.blit(card, (800, (HEIGHT / 2) - (hidden_deck_heigth / 2)))

        pygame.display.update()

    def check_input(self, pos):
        print('rect: ', self.hidden_deck_rect)
        print('clicked: ', pos)
        if self.hidden_deck_rect.collidepoint(pos):
            print('clicked hidden')
        else:
            print('not clicked')

    def check_drag(self, pos):
        print('dragging function...', pos)



