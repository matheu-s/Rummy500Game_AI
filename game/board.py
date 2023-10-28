import pygame
from time import sleep
from config.constants import *
from game.components.player import Player
from game.components.card import Card
from game.components.deck import Deck
from game.components.button import Button
from game.components.hand import Hand
from game.components.meld import Meld
from game.components.discard_pile import DiscardPile
from engine.srs import SRS


def get_font(size):
    return pygame.font.Font("assets/fonts/montserrat.ttf", size)


class Board:
    screen = None
    player_human = None
    player_engine = None
    human_points_acc = None
    engine_points_acc = None
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
    engine = None

    def __init__(self, screen, messenger):
        self.screen = screen
        self.messenger = messenger
        self.player_human = Player(is_human=True)
        self.player_engine = Player(is_human=False)
        self.human_points_acc = 0
        self.engine_points_acc = 0
        self.deck = Deck()
        self.discard_pile = DiscardPile()
        self.temp_melds = []
        self.temp_chosen_card = None
        self.hidden_deck_rect = None
        self.button_continue = None
        self.button_organize = None
        self.button_back = None
        self.turn = self.player_human
        self.action = Actions.DRAW.value
        self.engine = SRS()

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

        # Rendering points
        self.render_points()

    def check_input(self, mouse_pos):
        # Organize and Back button can be used anytime
        if self.button_back.is_clicked(mouse_pos):
            return False

        if self.is_game_finished():
            self.render_winner()

        if self.is_round_finished():
            self.restart_round()
            self.update_board()

        # Checking if player turn and action are corresponding to clicked object
        if self.turn == self.player_human:
            if self.action == Actions.DRAW.value:
                # Player decides to draw a card from hidden deck
                if self.hidden_deck_rect.collidepoint(mouse_pos):
                    if self.deck.length() == 0:
                        self.restart_round()
                        self.update_board()
                    self.player_human.hand.add_cards(self.deck.deal(1))
                    self.action = Actions.PROCEED.value
                    self.messenger.add_message('Click Continue to check possible melds', 2000)
                    self.update_board()
                    return True

                # Player decides to draw a card/cards from discard pile
                for i in range(len(self.discard_pile.cards)):
                    if self.discard_pile.cards[i].is_clicked(mouse_pos):
                        self.player_human.hand.add_cards(self.discard_pile.get_card(i))
                        self.action = Actions.PROCEED.value
                        self.messenger.add_message('Click Continue to check possible melds', 2000)
                        self.update_board()
                        break

            if self.action == Actions.PROCEED.value and self.button_continue.is_clicked(mouse_pos):
                mouse_pos = 0  # To not count this click twice for next action
                self.action = Actions.MELD_COMBINATION.value

            if self.action == Actions.MELD_COMBINATION.value:
                # Checking and rendering possible melds
                melds = self.player_human.hand.get_melds()
                if len(melds['seq']) or len(melds['group']):
                    # self.update_board(with_temp=True)
                    self.messenger.add_message('You can choose a meld to lay or simply continue', 2000)
                else:
                    self.messenger.add_message('No melds are possible', 1500)
                    self.action = Actions.CHOOSE_INDIVIDUAL_CARD.value
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
                    self.action = Actions.CHOOSE_INDIVIDUAL_CARD.value
                    self.messenger.add_message('You can try to lay cards from your hand into any melds on the table',
                                               2000)
                    return True

            if self.action == Actions.CHOOSE_INDIVIDUAL_CARD.value:
                # Erasing temp melds
                self.update_board(with_temp=False)

                for card in self.player_human.hand.cards:
                    if card.is_clicked(mouse_pos):
                        self.temp_chosen_card = card
                        self.messenger.add_message(f'Choose a meld to lay the {card.value} of {card.suit}.', 2000)
                        self.action = Actions.CHOOSE_INDIVIDUAL_MELD.value
                        return True

                if self.button_continue.is_clicked(mouse_pos):
                    self.action = Actions.DISCARD.value
                    self.messenger.add_message('Discard a card', 1500)
                    return True

            if self.action == Actions.CHOOSE_INDIVIDUAL_MELD.value:
                for meld in self.player_human.melds:
                    if meld.is_clicked(mouse_pos) \
                            and (self.player_human.hand.is_meld(meld.cards + [self.temp_chosen_card])
                                 or self.player_human.hand.is_meld([self.temp_chosen_card] + meld.cards)):
                        meld.add_card(self.temp_chosen_card)
                        self.player_human.hand.remove_card(self.temp_chosen_card)
                        self.update_board()
                        return True

                for meld in self.player_engine.melds:
                    if meld.is_clicked(mouse_pos) \
                            and (self.player_engine.hand.is_meld(meld.cards + [self.temp_chosen_card])
                                 or self.player_engine.hand.is_meld([self.temp_chosen_card] + meld.cards)):
                        meld.add_card(self.temp_chosen_card, self.temp_chosen_card.value)
                        self.player_human.hand.remove_card(self.temp_chosen_card)
                        self.player_human.add_indiv_points(self.temp_chosen_card.value)
                        self.update_board()
                        return True

                if self.button_continue.is_clicked(mouse_pos):
                    self.action = Actions.CHOOSE_INDIVIDUAL_CARD.value
                    self.messenger.add_message('You can try to lay cards from your hand into any melds on the table',
                                               2000)
                    return True

            if self.action == Actions.DISCARD.value:
                for card in self.player_human.hand.cards:
                    if card.is_clicked(mouse_pos):
                        self.player_human.hand.discard(card)
                        self.discard_pile.add_card(card)
                        self.messenger.add_message('Wait your turn', 2000)
                        self.update_board()
                        self.turn = self.player_engine
                        self.action = Actions.DRAW.value
                        break

        if self.turn == self.player_engine:
            self.engine_play()

        return True

    def render_cards(self):
        # Inserting hidden deck
        hidden_deck = pygame.image.load(f'assets/images/cards/back_side.png').convert()
        hidden_deck_width = 172 * 0.55
        hidden_deck_height = 244 * 0.55
        hidden_deck = pygame.transform.scale(hidden_deck, (int(hidden_deck_width), int(hidden_deck_height)))
        self.hidden_deck_rect = self.screen.blit(hidden_deck, (500, (HEIGHT / 2) - (hidden_deck_height / 2)))
        font = get_font(24)
        text_length_info = font.render(f'{self.deck.length()}', True, (255, 255, 255))
        self.screen.blit(text_length_info, (600, (HEIGHT / 2) - (hidden_deck_height / 2)))

        # Setting normal card sizes
        card_width = 125 * 0.55
        card_height = 182 * 0.55

        # TODO: Center hand cards automatically according to width... len(cards)*25 = width..
        # Rendering engine cards
        self.player_engine.hand.pos = 0
        hidden_img = pygame.image.load(f'assets/images/cards/back_side.png').convert()
        for i in self.player_engine.hand.cards:
            card = pygame.transform.scale(hidden_img, (int(card_width), int(card_height)))
            card_rect = self.screen.blit(card, (600 + self.player_engine.hand.pos, 20))
            i.set_rect(card_rect)
            self.player_engine.hand.pos += 25

        # Rendering human cards
        self.player_human.hand.sort()
        self.player_human.hand.pos = 0
        for i in self.player_human.hand.cards:
            card = pygame.transform.scale(i.image, (int(card_width), int(card_height)))
            card_rect = self.screen.blit(card, (600 + self.player_human.hand.pos, (HEIGHT) - (card_height + 20)))
            i.set_rect(card_rect)
            self.player_human.hand.pos += 25

        # Render the discard pile cards
        self.discard_pile.pos = 0
        height_level = 0
        for i in self.discard_pile.cards:
            card = pygame.transform.scale(i.image, (int(card_width), int(card_height)))
            card_rect = self.screen.blit(card, (650 + self.discard_pile.pos, (HEIGHT / 2)
                                                - (hidden_deck_height / 2) + height_level))
            i.set_rect(card_rect)
            self.discard_pile.pos += 25
            if self.discard_pile.pos > 250 and height_level == 0:
                height_level = 120
                self.discard_pile.pos = 0

    def render_buttons(self):
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
        card_width = 500 * 0.10
        card_height = 726 * 0.10

        # Rendering human melds
        width_counter = 0
        height_counter = 0
        for meld in self.player_human.melds:
            for card in meld.cards:
                card_display = pygame.transform.scale(card.image, (int(card_width), int(card_height)))
                card_rect = self.screen.blit(card_display, ((WIDTH - 350) + width_counter, 40 + height_counter))
                card.set_rect(card_rect)
                width_counter += 17
            height_counter += card_height + 20
            width_counter = 0

        # Rendering engine melds
        width_counter = 0
        height_counter = 0
        for meld in self.player_engine.melds:
            for card in meld.cards:
                card_display = pygame.transform.scale(card.image, (int(card_width), int(card_height)))
                card_rect = self.screen.blit(card_display, (150 + width_counter, 40 + height_counter))
                card.set_rect(card_rect)
                width_counter += 17
            height_counter += card_height + 20
            width_counter = 0

    def render_points(self):
        # Gathering points info
        human_points = self.player_human.get_points() + self.human_points_acc
        engine_points = self.player_engine.get_points() + self.engine_points_acc

        # Displaying points
        font = get_font(24)
        human_points_text = font.render(f'Your points: {human_points}', True, (255, 255, 255))
        engine_points_text = font.render(f'Engine points: {engine_points}', True, (255, 255, 255))
        self.screen.blit(human_points_text, (WIDTH - 200, 5))
        self.screen.blit(engine_points_text, (10, 5))

    def update_board(self, with_temp=False):
        self.screen.fill(GREEN_TABLE)
        self.render_buttons()
        self.render_cards()
        self.render_melds()
        self.render_points()
        if with_temp:
            self.render_temp_melds()

    def render_temp_melds(self):
        self.temp_melds = []
        card_width = 500 * 0.150
        card_height = 726 * 0.150
        width_counter = 0
        height_counter = 0

        melds = self.player_human.hand.get_melds()
        for key in melds:
            for meld in melds[key]:
                meld_cards = []
                for card in meld:
                    new_card = Card(card.value, card.suit)
                    card_display = pygame.transform.scale(new_card.image, (int(card_width), int(card_height)))
                    card_rect = self.screen.blit(card_display, (100 + width_counter, 20 + height_counter))
                    new_card.set_rect(card_rect)
                    meld_cards.append(new_card)
                    width_counter += 20
                self.temp_melds.append(Meld(meld_cards, key))
                height_counter += 150
                width_counter = 0

    def get_board_data(self):
        self.player_engine.hand.sort()
        self.player_human.hand.sort()

        seen_cards = []
        all_cards = []
        for suit in SUITS:
            for value in range(1, 14):
                all_cards.append(f'{value}{suit}')

        engine_cards = []
        for card in self.player_engine.hand.cards:
            engine_cards.append(f'{card.value}{card.suit}')
            seen_cards.append(f'{card.value}{card.suit}')

        engine_melds = []
        for meld in self.player_engine.melds:
            for card in meld.cards:
                engine_melds.append(f'{card.value}{card.suit}')
                seen_cards.append(f'{card.value}{card.suit}')

        human_melds = []
        for meld in self.player_human.melds:
            for card in meld.cards:
                human_melds.append(f'{card.value}{card.suit}')
                seen_cards.append(f'{card.value}{card.suit}')

        discard_pile = []
        for card in self.discard_pile.cards:
            discard_pile.append(f'{card.value}{card.suit}')
            seen_cards.append(f'{card.value}{card.suit}')

        unseen_cards = [card for card in all_cards if card not in seen_cards]

        board_data = {
            'engine_points': self.player_engine.get_points(),
            'engine_cards': engine_cards,
            'engine_melds': engine_melds,
            'human_melds': human_melds,
            'human_hand_length': len(self.player_human.hand.cards),
            'human_points': self.player_human.get_points(),
            'discard_pile_cards': discard_pile,
            'all_cards': all_cards,
            'seen_cards': seen_cards,
            'unseen_cards': unseen_cards
        }

        return board_data

    def engine_play(self):
        self.engine.update_data(self.get_board_data())
        if self.action == Actions.DRAW.value:
            # Drawing card action
            move = self.engine.get_draw_move()
            if move['action'] == Actions.DRAW_HIDDEN.value:
                # Engine decides to draw from hidden pile
                self.player_engine.hand.add_cards(self.deck.deal(1))
            else:
                # Engine decides to draw from discard pile
                chosen_card_index = move['target']
                self.player_engine.hand.add_cards(self.discard_pile.get_card(int(chosen_card_index)))
                print('got from discard pile!')

            self.action = Actions.MELD_COMBINATION.value
            self.engine.update_data(self.get_board_data())
            self.update_board()

        if self.action == Actions.MELD_COMBINATION.value:
            # Laying melds
            melds = self.engine.get_meld_combinations_move()
            for key in melds:
                for meld in melds[key]:
                    cards_arr = []
                    for card in meld:
                        card_created = Card(int(card[:-1]), card[-1:])
                        cards_arr.append(card_created)
                    meld = Meld(cards_arr, key)
                    self.player_engine.hand.meld(meld)
                    self.player_engine.melds.append(meld)
            self.action = Actions.MELD_INDIVIDUAL.value
            self.engine.update_data(self.get_board_data())
            self.update_board()

        if self.action == Actions.MELD_INDIVIDUAL.value:
            # Laying individual cards into existing melds

            for card in self.player_engine.hand.cards:
                melded = False
                for meld in self.player_engine.melds:
                    if self.player_engine.hand.is_meld(meld.cards + [card]):
                        meld.add_card(card)
                        self.player_engine.hand.remove_card(card)
                        melded = True
                        break
                    if self.player_engine.hand.is_meld([card] + meld.cards):
                        meld.add_card(card)
                        self.player_engine.hand.remove_card(card)
                        melded = True
                        break

                if melded:
                    continue

                for meld2 in self.player_human.melds:
                    if self.player_engine.hand.is_meld(meld2.cards + [card]):
                        meld2.add_card(card, card.value)
                        self.player_engine.hand.remove_card(card)
                        self.player_engine.add_indiv_points(card.value)
                        break
                    if self.player_engine.hand.is_meld([card] + meld2.cards):
                        meld2.add_card(card, card.value)
                        self.player_engine.hand.remove_card(card)
                        self.player_engine.add_indiv_points(card.value)
                        break

            self.update_board()
            self.engine.update_data(self.get_board_data())
            self.action = Actions.DISCARD.value

        if self.action == Actions.DISCARD.value:
            # Discarding
            discard_card = self.engine.get_discard_move()['target']
            for card in self.player_engine.hand.cards:
                if int(discard_card[:-1]) == card.value and discard_card[-1:] == card.suit:
                    self.player_engine.hand.discard(card)
                    self.discard_pile.add_card(card)
                    break

            # Setting turn back to human
            self.turn = self.player_human
            self.action = Actions.DRAW.value
            self.engine.update_data(self.get_board_data())
            self.update_board()
            return

        return True

    def is_round_finished(self):
        return len(self.player_human.hand.cards) == 0 \
            or len(self.player_engine.hand.cards) == 0

    def is_game_finished(self):
        return self.player_engine.get_points() + self.engine_points_acc > 499 \
            or self.player_human.get_points() + self.human_points_acc > 499

    def restart_round(self):
        # Restarting the deck
        self.deck = Deck()
        self.deck.shuffle()

        # Restarting discard pile
        self.discard_pile = DiscardPile()
        self.discard_pile.add_card(self.deck.deal(1))

        # Saving points and restarting players
        self.human_points_acc += self.player_human.get_points()
        self.engine_points_acc += self.player_engine.get_points()
        self.subtract_points()
        print('round restarted')
        print('engine points: ', self.engine_points_acc)
        print('human points: ', self.human_points_acc)
        sleep(20) # take to check board and screenshot before restarting

        self.player_human = Player(is_human=True)
        self.player_human.set_hand(Hand(self.deck.deal(13)))

        self.player_engine = Player(is_human=False)
        self.player_engine.set_hand(Hand(self.deck.deal(13)))

    def render_winner(self):
        # TODO: Render winner screen
        print('winner')

    def subtract_points(self):
        """" Subtracts points from the cards present in hand at the end of the round\""""

        engine_lost_points = 0
        for card in self.player_engine.hand.cards:
            if int(card.value) > 10:
                engine_lost_points += 10
                return
            engine_lost_points += 5
        self.engine_points_acc = self.engine_points_acc - engine_lost_points

        human_lost_points = 0
        for card in self.player_human.hand.cards:
            if int(card.value) > 10:
                human_lost_points += 10
                return
            human_lost_points += 5
        self.human_points_acc = self.human_points_acc - human_lost_points
