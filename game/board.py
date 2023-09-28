import pygame, time, os, sys
from config.constants import *
from game.player import Player
from game.card import Card
from game.deck import Deck
from game.button import Button
from game.hand import Hand
from game.meld import Meld
from game.discard_pile import DiscardPile


def get_font(size):
    return pygame.font.Font("assets/fonts/montserrat.ttf", size)


class Board:
    screen = None
    player_human = None
    player_engine = None
    hidden_deck_rect = None
    discard_pile = None
    temp_melds = None
    temp_chosen_card = None
    messenger = None
    button_organize = None
    button_continue = None
    button_back = None
    deck = None
    turn = None
    action = None

    def __init__(self, screen, messenger):
        self.screen = screen
        self.messenger = messenger
        self.player_human = Player(is_human=True)
        self.player_engine = Player(is_human=False)
        self.deck = Deck()
        self.discard_pile = DiscardPile()
        self.temp_melds = []
        self.temp_chosen_card = None
        self.hidden_deck_rect = None
        self.button_continue = None
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
                    self.action = 'proceed'
                    self.messenger.add_message('Click Continue to check possible melds', 2000)
                    self.update_board()
                    return True

                # Player decides to draw a card/cards from discard pile
                for i in range(len(self.discard_pile.cards)):
                    if self.discard_pile.cards[i].is_clicked(mouse_pos):
                        self.player_human.hand.add_cards(self.discard_pile.get_card(self.discard_pile.cards[i], i))
                        self.action = 'proceed'
                        self.messenger.add_message('Click Continue to check possible melds', 2000)
                        self.update_board()
                        break

            if self.action == 'proceed' and self.button_continue.is_clicked(mouse_pos):
                mouse_pos = 0  # To not count this click twice for next action
                self.action = 'meld'

            if self.action == 'meld':
                # Checking and rendering possible melds
                seq, group = self.player_human.hand.get_melds()
                if len(seq) or len(group):
                    # self.update_board(with_temp=True)
                    self.messenger.add_message('You can choose a meld to lay or simply continue', 2000)
                else:
                    self.messenger.add_message('No melds are possible', 1500)
                    self.action = 'meld_card'
                    return True

                # Check if meld is clicked and add it to player
                for meld in self.temp_melds:
                    if meld.is_clicked(mouse_pos):
                        self.player_human.hand.meld(meld)
                        self.player_human.melds.append(meld)
                        self.temp_melds.remove(meld)

                self.update_board(with_temp=True)

                if mouse_pos == 0:
                    return True
                # Player chooses to not lay down
                if self.button_continue.is_clicked(mouse_pos):
                    self.action = 'meld_card'
                    self.messenger('You can try to lay cards from your hand into any melds on the table', 2000)
                    return True

            if self.action == 'meld_card':
                # Erasing temp melds
                self.update_board(with_temp=False)

                for card in self.player_human.hand.cards:
                    if card.is_clicked(mouse_pos):
                        self.temp_chosen_card = card
                        self.messenger.add_message(f'Choose a meld to lay the {card.value} of {card.suit}.', 2000)
                        return True

                for meld in self.player_human.melds:
                    if meld.is_clicked(mouse_pos) \
                            and (self.player_human.hand.is_meld(meld.cards + [self.temp_chosen_card])
                                 or self.player_human.hand.is_meld([self.temp_chosen_card] + meld.cards)):
                        meld.add_card(self.temp_chosen_card)
                        self.player_human.hand.discard(self.temp_chosen_card)
                        self.update_board()
                        return True

                for meld in self.player_engine.melds:
                    if meld.is_clicked(mouse_pos) \
                            and (self.player_engine.hand.is_meld(meld.cards + [self.temp_chosen_card])
                                 or self.player_engine.hand.is_meld([self.temp_chosen_card] + meld.cards)):
                        meld.add_card(self.temp_chosen_card)
                        self.player_engine.hand.discard(self.temp_chosen_card)
                        self.update_board()
                        return True

                if self.button_continue.is_clicked(mouse_pos):
                    self.action = 'discard'
                    self.messenger.add_message('Discard a card', 1500)
                    return True

            if self.action == 'discard':
                for card in self.player_human.hand.cards:
                    if card.is_clicked(mouse_pos):
                        self.player_human.hand.discard(card)
                        self.discard_pile.add_card(card)
                        self.messenger.add_message('Wait your turn', 2000)
                        self.update_board()
                        self.turn = self.player_engine
                        self.action = 'draw_card'
                        break

        return True

    def sort_hand(self):
        self.player_human.hand.sort()
        self.player_human.hand.pos = 0
        self.render_cards()

    def render_cards(self):
        # Inserting hidden deck
        hidden_deck = pygame.image.load(f'assets/images/cards/back_side.png').convert()
        hidden_deck_width = 686 * 0.15
        hidden_deck_heigth = 976 * 0.15
        hidden_deck = pygame.transform.scale(hidden_deck, (int(hidden_deck_width), int(hidden_deck_heigth)))
        self.hidden_deck_rect = self.screen.blit(hidden_deck, (650, (HEIGHT / 2) - (hidden_deck_heigth / 2)))

        # Setting normal card sizes
        card_width = 500 * 0.204
        card_height = 726 * 0.204
        hidden_deck_heigth = 976 * 0.15

        # TODO: Center hand cards automatically accroding to width... len(cards)*25 = width..
        # Rendering engine cards
        self.player_engine.hand.pos = 0
        hidden_img = pygame.image.load(f'assets/images/cards/back_side.png').convert()
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
        self.button_organize = Button(image=None, pos=(WIDTH - 275, HEIGHT - 50),
                                      text_input="Organize", font=get_font(20), base_color="White",
                                      hovering_color="Blue")
        self.button_organize.update(self.screen)

        # Button to continue the flow
        self.button_continue = Button(image=None, pos=(WIDTH - 150, HEIGHT - 50),
                                      text_input="Continue", font=get_font(20), base_color="White",
                                      hovering_color="Blue")
        self.button_continue.update(self.screen)

        # Back to menu button
        self.button_back = Button(image=None, pos=(WIDTH - 50, HEIGHT - 50),
                                  text_input="Back", font=get_font(20), base_color="White", hovering_color="Blue")
        self.button_back.update(self.screen)

    def render_melds(self):
        card_width = 500 * 0.150
        card_height = 726 * 0.150

        # Rendering human melds
        width_counter = 0
        height_counter = 0
        for meld in self.player_human.melds:
            for card in meld.cards:
                card_display = pygame.transform.scale(card.image, (int(card_width), int(card_height)))
                card_rect = self.screen.blit(card_display, ((WIDTH - 350) + width_counter, 40 + height_counter))
                card.set_rect(card_rect)
                width_counter += 20
            height_counter += 150
            width_counter = 0

        # Rendering engine melds
        width_counter = 0
        height_counter = 0
        for meld in self.player_engine.melds:
            for card in meld.cards:
                card_display = pygame.transform.scale(card.image, (int(card_width), int(card_height)))
                card_rect = self.screen.blit(card_display, 150 + width_counter, 40 + height_counter)
                card.set_rect(card_rect)
                width_counter += 20
            height_counter += 150
            width_counter = 0

    def update_board(self, with_temp=False):
        self.screen.fill(GREEN_TABLE)
        self.render_buttons()
        self.render_cards()
        self.render_melds()
        if with_temp:
            self.render_temp_melds()

    def render_temp_melds(self):
        self.temp_melds = []
        card_width = 500 * 0.150
        card_height = 726 * 0.150
        width_counter = 0
        height_counter = 0

        groups, seqs = self.player_human.hand.get_melds()
        for meld in groups:
            meld_cards = []
            for card in meld:
                new_card = Card(card.value, card.suit)
                card_display = pygame.transform.scale(new_card.image, (int(card_width), int(card_height)))
                card_rect = self.screen.blit(card_display, (100 + width_counter, 20 + height_counter))
                new_card.set_rect(card_rect)
                meld_cards.append(new_card)
                width_counter += 20
            self.temp_melds.append(Meld(meld_cards, 'group'))
            height_counter += 150
            width_counter = 0

        for meld in seqs:
            meld_cards = []
            for card in meld:
                new_card = Card(card.value, card.suit)
                card_display = pygame.transform.scale(new_card.image, (int(card_width), int(card_height)))
                card_rect = self.screen.blit(card_display, (100 + width_counter, 20 + height_counter))
                new_card.set_rect(card_rect)
                meld_cards.append(new_card)
                width_counter += 20
            self.temp_melds.append(Meld(meld_cards, 'seq'))
            height_counter += 150
            width_counter = 0
