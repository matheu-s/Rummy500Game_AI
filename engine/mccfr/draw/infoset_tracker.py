from typing import NewType, Dict, List, Callable, cast

from labml import monit, tracker, logger, experiment
from labml.configs import BaseConfigs, option
from engine.mccfr.draw.infoset import InfoSet


# A player $i \in N$ where $N$ is the set of players
Player = NewType('Player', int)
# Action $a$, $A(h) = {a: (h, a) \in H}$ where $h \in H$ is a non-terminal [history](#History)
Action = NewType('Action', str)


class InfoSetTracker:
    """
    ### Information set tracker

    This is a small helper class to track data from information sets
    """

    def __init__(self):
        """
        Set tracking indicators
        """
        tracker.set_histogram(f'strategy.*')
        tracker.set_histogram(f'average_strategy.*')
        tracker.set_histogram(f'regret.*')

    def __call__(self, info_sets: Dict[str, InfoSet]):
        """
        Track the data from all information sets
        """
        for I in info_sets.values():
            avg_strategy = I.get_average_strategy()
            for a in I.actions():
                tracker.add({
                    f'strategy.{I.key}.{a}': I.strategy[a],
                    f'average_strategy.{I.key}.{a}': avg_strategy[a],
                    f'regret.{I.key}.{a}': I.regret[a],
                })
