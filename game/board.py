import pygame, time, os, sys
from config.constants import *
from game.player import Player
from game.deck import Deck
from game.button import Button
from game.hand import Hand
from game.discard_pile import DiscardPile


def get_font(size):
    return pygame.font.Font("assets/fonts/montserrat.ttf", size)


class Board:
    screen = None
    player_human = None
    player_engine = None
    hidden_deck_rect = None
    discard_pile = None
    button_organize = None
    button_lay = None
    button_back = None
    deck = None
    turn = None
    action = None

    def __init__(self, screen):
        self.screen = screen
        self.player_human = Player(is_human=True)
        self.player_engine = Player(is_human=False)
        self.deck = Deck()
        self.discard_pile = DiscardPile()
        self.hidden_deck_rect = None
        self.button_lay = None
        self.button_organize = None
        self.button_back = None
        self.turn = self.player_human
        self.action = 'draw_card'

    def start_board(self):
        self.deck.shuffle()

        # Dealing cards
        self.player_human.set_hand(Hand(self.deck.deal(13)))
        self.player_engine.set_hand(Hand(self.deck.deal(13)))
        self.discard_pile.add_card(self.deck.deal(1))

        # Rendering cards
        self.render_cards()

        # Rendering buttons
        self.render_buttons()

    def check_input(self, mouse_pos):
        # Organize and Back button can be used anytime
        if self.button_back.is_clicked(mouse_pos):
            return False
        if self.button_organize.is_clicked(mouse_pos):
            self.sort_hand()

        # Checking if player turn and action are corresponding to clicked object
        if self.turn == self.player_human:
            if self.action == 'draw_card':
                # Player decides to draw a card from hidden deck
                if self.hidden_deck_rect.collidepoint(mouse_pos):
                    self.player_human.hand.add_cards(self.deck.deal(1))
                    self.action = 'meld'
                    self.update_board()
                    return

                # Player decides to draw a card/cards from discard pile
                for i in range(len(self.discard_pile.cards)):
                    if self.discard_pile.cards[i].is_clicked(mouse_pos):
                        print('getting from discard pile')
                        self.player_human.hand.add_cards(self.discard_pile.get_card(self.discard_pile.cards[i], i))
                        self.action = 'meld'
                        self.update_board()
                        break

            if self.action == 'meld':
                # Player checks possible melds
                if self.button_lay.is_clicked(mouse_pos):
                    possible_seqs, possible_groups = self.player_human.hand.get_melds()
                    for i in possible_seqs:
                        print('possible seq')
                        for j in i:
                            print(j.value, ' ', j.suit)

            if self.action == 'discard':
                for i in self.player_human.hand.cards:
                    if i.is_clicked(mouse_pos):
                        print('mouse_pos: ', mouse_pos)
                        print('clicked: ', i.value, i.suit, i.rect)

        return True

    def check_drag(self, pos):
        print('dragging function...', pos)

    def sort_hand(self):
        self.player_human.hand.sort()
        self.player_human.hand.pos = 0
        self.render_cards()

    def render_cards(self):
        # Inserting hidden deck
        hidden_deck = pygame.image.load(f'assets/images/cards/back_side.png')
        hidden_deck_width = 686 * 0.15
        hidden_deck_heigth = 976 * 0.15
        hidden_deck = pygame.transform.scale(hidden_deck, (int(hidden_deck_width), int(hidden_deck_heigth)))
        self.hidden_deck_rect = self.screen.blit(hidden_deck, (650, (HEIGHT / 2) - (hidden_deck_heigth / 2)))

        # Setting normal card sizes
        card_width = 500 * 0.204
        card_height = 726 * 0.204
        hidden_deck_heigth = 976 * 0.15

        # Rendering engine cards
        self.player_engine.hand.pos = 0
        hidden_img = pygame.image.load(f'assets/images/cards/back_side.png')
        for i in self.player_engine.hand.cards:
            card = pygame.transform.scale(hidden_img, (int(card_width), int(card_height)))
            card_rect = self.screen.blit(card, (600 + self.player_engine.hand.pos, 20))
            i.set_rect(card_rect)
            self.player_engine.hand.pos += 25

        # Rendering human cards
        self.player_human.hand.pos = 0
        for i in self.player_human.hand.cards:
            card = pygame.transform.scale(i.image, (int(card_width), int(card_height)))
            card_rect = self.screen.blit(card, (600 + self.player_human.hand.pos, (HEIGHT) - (card_height + 20)))
            i.set_rect(card_rect)
            self.player_human.hand.pos += 25

        # Render the discard pile cards
        self.discard_pile.pos = 0
        for i in self.discard_pile.cards:
            card = pygame.transform.scale(i.image, (int(card_width), int(card_height)))
            card_rect = self.screen.blit(card, (800 + self.discard_pile.pos, (HEIGHT / 2) - (hidden_deck_heigth / 2)))
            i.set_rect(card_rect)
            self.discard_pile.pos += 25

    def render_buttons(self):
        # Button to organize human cards
        self.button_organize = Button(image=None, pos=(WIDTH - 300, HEIGHT - 50),
                                      text_input="Organize", font=get_font(20), base_color="White",
                                      hovering_color="Blue")
        self.button_organize.update(self.screen)

        # Button to lay human cards
        self.button_lay = Button(image=None, pos=(WIDTH - 450, HEIGHT - 50),
                                 text_input="Lay down", font=get_font(20), base_color="White", hovering_color="Blue")
        self.button_lay.update(self.screen)

        # Back to menu button
        self.button_back = Button(image=None, pos=(WIDTH - 150, HEIGHT - 50),
                                  text_input="Back", font=get_font(20), base_color="White", hovering_color="Blue")
        self.button_back.update(self.screen)

    def update_board(self):
        self.screen.fill(GREEN_TABLE)
        self.render_buttons()
        self.render_cards()

    def display_possible_melds(self):
        print('melds...')
