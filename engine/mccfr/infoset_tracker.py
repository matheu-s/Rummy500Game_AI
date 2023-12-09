from labml import tracker
from typing import NewType, Dict
from engine.mccfr.infoset import InfoSet


class InfoSetTracker:
    def __init__(self):
        tracker.set_histogram(f'strategy.*')
        tracker.set_histogram(f'average_strategy.*')
        tracker.set_histogram(f'regret.*')

    def __call__(self, info_sets: Dict[str, InfoSet]):
        for I in info_sets.values():
            avg_strategy = I.get_average_strategy()
            for a in I.actions():
                tracker.add({
                    f'strategy.{I.key}.{a}': I.strategy[a],
                    f'average_strategy.{I.key}.{a}': avg_strategy[a],
                    f'regret.{I.key}.{a}': I.regret[a],
                })
