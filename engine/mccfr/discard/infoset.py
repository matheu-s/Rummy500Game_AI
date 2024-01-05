from typing import List, cast, Dict

import numpy as np

from labml import experiment
from labml.configs import option
from labml_nn.cfr import History as _History, InfoSet as _InfoSet, Action, Player, CFRConfigs
from labml_nn.cfr.infoset_saver import InfoSetSaver

# Rummy discard actions d (discards card immediately), s (saves the card in hand and discard other when possible)
ACTIONS = cast(List[Action], ['d', 's'])


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
        draw_hidden = self.cumulative_strategy[cast(Action, 's')] / total
        return f'{draw_hidden * 100: .1f}%'
