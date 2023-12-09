from config.constants import SUITS
from engine.srs import SRS
from random import shuffle


class Game:
    data = None
    helper = None
    player = None

    def __init__(self):
        self.data = None
        self.helper = SRS()
        self.player = 0

    def get_new_game(self):
        """Simulates a new game and passes data to helper"""

        print("NEW GAME!")

        # Creating and shuffling deck
        deck = []
        for suit in SUITS:
            for i in range(1, 14):
                deck.append(str(i) + suit)
        shuffle(deck)

        # Dealing cards
        p0_hand = deck[-13:]
        deck = deck[:-13]
        p1_hand = deck[-13:]
        deck = deck[:-13]

        discard_pile = [deck.pop()]

        data = {
            'p0_points': 0,
            'p1_points': 0,
            'p0_cards': p0_hand,
            'p1_cards': p1_hand,
            'p0_melds': [],
            'p1_melds': [],
            'p1_hand_length': len(p1_hand),
            'deck_cards': deck,
            'discard_pile_cards': discard_pile
        }

        self.helper.update_data(data)
        self.data = data

        return data

    def draw_hidden(self):
        # Getting from deck and updating deck and hands
        card = self.data['deck_cards'].pop()

        self.data[f'p{self.player}_cards'] += [card]

        # Play rest of round according to basic rules
        self.finish_the_play()

        return self.data

    def draw_discard(self):
        # Playing 1 round after discard pile pick (always as deep as possible)

        deep_picks = self.helper.data_helper.get_possible_discard_picks(self.data['discard_pile_cards'], self.data[f'p{self.player}_cards'])
        mandatory_meld = None

        if len(deep_picks):
            # If there is a deep pick with melds...
            mandatory_meld = deep_picks[0]['mandatory_meld']
            discard_pick = self.data['discard_pile_cards'].pop(deep_picks[0]['card_index'])
        else:
            # Pick top card of discard
            discard_pick = self.data['discard_pile_cards'].pop()

        self.data[f'p{self.player}_cards'] += [discard_pick]

        if mandatory_meld:
            print('mandatory meld... ', mandatory_meld)
            print(self.data[f'p{self.player}_cards'])
            for card_in_meld in mandatory_meld:
                try:
                    self.data[f'p{self.player}_cards'].remove(card_in_meld)
                except ValueError:
                    print('Additional card from discard pile')
            self.data[f'p{self.player}_melds'].append(mandatory_meld)

        # Play rest of round according to basic rules
        self.finish_the_play()

        return self.data

    def finish_the_play(self):
        self.update_points()

        # Melding everything
        melds = self.helper.get_meld_combinations_move()['melds']
        for meld in melds:
            for card in meld:
                self.data[f'p{self.player}_cards'].remove(card)
            self.data[f'p{self.player}_melds'].append(meld)

        self.update_points()

        # Discarding
        discard_card = self.helper.get_discard_move(self.player)['target']
        self.data[f'p{self.player}_cards'].remove(discard_card)
        self.data['discard_pile_cards'].append(discard_card)


    def is_terminal(self, data):
        if len(data['p0_cards']) == 0 \
                or len(data['p1_cards']) == 0 \
                or len(data['deck_cards']) == 0 \
                or data['p1_points'] > 200 \
                or data['p0_points'] > 200:
            print('terminal',  data['p0_points'], data['p1_points'])
            # print(data['p0_cards'])
            # print(data['p1_cards'])
            # print(data['discard_pile_cards'])
            # print(len(data['deck_cards']))
            return True
        print('not terminal ', data['p0_points'], data['p1_points'])
        # print(data['p0_cards'])
        # print(data['p1_cards'])
        # print(data['discard_pile_cards'])
        # print(len(data['deck_cards']))

        return False

    def change_player(self):
        self.player = 1 - self.player

    def update_points(self):
        p0_points = 0
        p1_points = 0
        for meld in self.data['p0_melds']:
            p0_points += self.helper.data_helper.calculate_meld_points(meld)
        for meld in self.data['p1_melds']:
            p1_points += self.helper.data_helper.calculate_meld_points(meld)

        self.data['p0_points'] = p0_points
        self.data['p1_points'] = p1_points


game = Game()
