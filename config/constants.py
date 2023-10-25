from enum import Enum

# Main screen size
WIDTH, HEIGHT = 1600*0.8, 900*0.8

# Colors
GREEN = (127, 166, 80)
GREY = (106, 133, 136)
BLACK = (1, 1, 1)
YELLOW = (243, 199, 13)
RED = (255, 0, 0)
LIGHT_RED = (255, 109, 106)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
GREEN_TABLE = (0, 81, 44)

# General
FPS = 60

# Cards
SUITS = ['c', 'h', 's', 'd']


# Actions
class Actions(Enum):
    DRAW = '1'
    DRAW_HIDDEN = '2'
    DRAW_DISCARD = '3'
    MELD_COMBINATION = '4'
    CHOOSE_INDIVIDUAL_CARD = '5'
    CHOOSE_INDIVIDUAL_MELD = '6'
    DISCARD = '7'
    PROCEED = '8'
    MELD_INDIVIDUAL = '9'


