from typing import NewType, List, cast
from labml_nn.cfr import InfoSet as _InfoSet
import sys

sys.setrecursionlimit(999999999)

Player = NewType('Player', int)
Action = NewType('Action', str)

# d = Draw from discard pile / h = Draw from hidden pile
ACTIONS = cast(List[Action], ['d', 'h'])

PLAYERS = cast(List[Player], [0, 1])


class InfoSet(_InfoSet):
    key = str
    strategy = dict[Action, float]
    regret = dict[Action, float]
    cumulative_strategy = dict[Action, float]

    def __init__(self, key: str):
        self.key = key
        self.regret = {a: 0 for a in self.actions()}  # {'hidden': 0, 'pile': 0}
        self.cumulative_strategy = {a: 0 for a in self.actions()}
        self.calculate_strategy()

    def actions(self) -> List[Action]:
        return ACTIONS

    def __repr__(self):
        total = sum(self.cumulative_strategy.values())
        total = max(total, 1e-6)
        bet = self.cumulative_strategy[cast(Action, 'h')] / total
        return f'{bet * 100: .1f}%'

    def to_dict(self):
        return {
            'key': self.key,
            'regret': self.regret,
            'average_strategy': self.cumulative_strategy,
        }

    def load_dict(self, data: dict[str, any]):
        self.regret = data['regret']
        self.cumulative_strategy = data['average_strategy']
        self.calculate_strategy()

    def calculate_strategy(self):
        regret = {a: max(r, 0) for a, r in self.regret.items()}
        regret_sum = sum(regret.values())
        if regret_sum > 0:
            self.strategy = {a: r / regret_sum for a, r in regret.items()}
        else:
            count = len(list(a for a in self.regret))
            self.strategy = {a: 1 / count for a, r in regret.items()}

    def get_average_strategy(self):
        cum_strategy = {a: self.cumulative_strategy.get(a, 0.) for a in self.actions()}
        strategy_sum = sum(cum_strategy.values())

        if strategy_sum > 0:
            return {a: s / strategy_sum for a, s in cum_strategy.items()}
        else:
            count = len(list(a for a in cum_strategy))
            return {a: 1 / count for a, r in cum_strategy.items()}

