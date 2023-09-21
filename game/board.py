import pygame, time, os, sys
from config.constants import *
from game.player import Player
from game.deck import Deck
from game.button import Button
from game.hand import Hand


def get_font(size):
    return pygame.font.Font("assets/fonts/montserrat.ttf", size)


class Board:
    screen = None
    player_human = None
    player_engine = None
    hidden_deck_rect = None
    pile = None
    button_organize = None
    button_lay = None
    deck = None
    turn = None
    pile_cards_pos = 0

    def __init__(self, screen):
        self.screen = screen
        self.player_human = Player(is_human=True)
        self.player_engine = Player(is_human=False)
        self.hidden_deck_rect = None
        self.button_lay = None
        self.button_organize = None
        self.deck = Deck()
        self.turn = self.player_human
        self.pile = []
        self.pile_cards_pos = 0
        self.human_hand_pos = 0
        self.engine_hand_pos = 0

    def start_board(self):
        # Inserting hidden deck
        hidden_deck = pygame.image.load(f'assets/images/cards/back_side.png')
        hidden_deck_width = 686 * 0.15
        hidden_deck_heigth = 976 * 0.15
        hidden_deck = pygame.transform.scale(hidden_deck, (int(hidden_deck_width), int(hidden_deck_heigth)))
        self.hidden_deck_rect = self.screen.blit(hidden_deck, (650, (HEIGHT / 2) - (hidden_deck_heigth / 2)))

        self.deck.shuffle()

        # Dealing cards
        self.player_human.set_hand(Hand(self.deck.deal(13)))
        self.player_engine.set_hand(Hand(self.deck.deal(13)))
        self.pile = self.deck.deal()

        # Rendering cards
        self.render_cards(player='human')
        self.render_cards(player='engine')
        self.render_cards(player='pile')

        # Button to organize human cards
        self.button_organize = Button(image=None, pos=(WIDTH - 300, HEIGHT - 50),
                                      text_input="Organize", font=get_font(20), base_color="White",
                                      hovering_color="Blue")
        self.button_organize.update(self.screen)

        # Button to lay human cards
        self.button_lay = Button(image=None, pos=(WIDTH - 450, HEIGHT - 50),
                                 text_input="Lay down", font=get_font(20), base_color="White", hovering_color="Blue")
        self.button_lay.update(self.screen)
        pygame.display.update()

    def check_input(self, mouse_pos):
        if self.hidden_deck_rect.collidepoint(mouse_pos):
            print('clicked hidden')
        elif self.button_organize.isClicked(mouse_pos):
            self.sort_hand()
        elif self.button_lay.isClicked(mouse_pos) and self.turn == self.player_human:
            possible_seqs, possible_groups = self.player_human.hand.get_melds()
            for i in possible_seqs:
                print('possible seq')
                for j in i:
                    print(j.value, ' ', j.suit)

    def check_drag(self, pos):
        print('dragging function...', pos)

    def sort_hand(self):
        self.player_human.hand.sort()
        self.player_human.hand.pos = 0
        self.render_cards(player='human')

    def render_cards(self, player):
        card_width = 500 * 0.204
        card_height = 726 * 0.204
        hidden_deck_heigth = 976 * 0.15

        if player == 'engine':
            hidden_img = pygame.image.load(f'assets/images/cards/back_side.png')
            for i in self.player_engine.hand.cards:
                card = pygame.transform.scale(hidden_img, (int(card_width), int(card_height)))
                self.screen.blit(card, (600 + self.player_engine.hand.pos, 20))
                self.player_engine.hand.pos += 25
        elif player == 'human':
            for i in self.player_human.hand.cards:
                card = pygame.transform.scale(i.image, (int(card_width), int(card_height)))
                self.screen.blit(card, (600 + self.player_human.hand.pos, (HEIGHT) - (card_height + 20)))
                self.player_human.hand.pos += 25
        else:
            # Render to the pile
            for i in self.pile:
                card = pygame.transform.scale(i.image, (int(card_width), int(card_height)))
                self.screen.blit(card, (800 + self.pile_cards_pos, (HEIGHT / 2) - (hidden_deck_heigth / 2)))
                self.pile_cards_pos += 25
