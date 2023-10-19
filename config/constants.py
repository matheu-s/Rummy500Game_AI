from enum import Enum

# Main screen size
WIDTH, HEIGHT = (1600 / 1.2), (900 / 1.2)

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
SUITS = ['clubs', 'hearts', 'spades', 'diamonds']


# Actions
class Actions(Enum):
    DRAW = 'draw_card'
    DRAW_HIDDEN = 'draw_hidden'
    DRAW_DISCARD = 'draw_discard'
    MELD_COMBINATION = 'meld'
    MELD_INDIVIDUAL = 'meld_card'
    DISCARD = 'discard'
    PROCEED = 'proceed'

