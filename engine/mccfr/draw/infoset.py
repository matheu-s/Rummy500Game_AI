from typing import List, cast, Dict

import numpy as np

from labml import experiment
from labml.configs import option
from labml_nn.cfr import History as _History, InfoSet as _InfoSet, Action, Player, CFRConfigs
from labml_nn.cfr.infoset_saver import InfoSetSaver

# Rummy draw actions are draw from hidden pile (`h`) or draw from discard pile (`d`)
ACTIONS = cast(List[Action], ['h', 'd'])


class InfoSet(_InfoSet):
    """
    ## [Information set](../index.html#InfoSet)
    """

    @staticmethod
    def from_dict(data: Dict[str, any]) -> 'InfoSet':
        """Does not support save/load"""
        pass

    def actions(self) -> List[Action]:
        """
        Return the list of actions. Terminal states are handled by `History` class.
        """
        return ACTIONS

    def __repr__(self):
        """
        Human readable string representation - it gives the drawing hidden percentage for the found strategy in each IS
        """
        total = sum(self.cumulative_strategy.values())
        total = max(total, 1e-6)
        draw_hidden = self.cumulative_strategy[cast(Action, 'h')] / total
        return f'{draw_hidden * 100: .1f}%'
