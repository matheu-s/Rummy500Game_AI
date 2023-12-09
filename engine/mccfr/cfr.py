from typing import Callable, Dict, NewType, cast
from labml import monit, tracker, logger, experiment
from engine.mccfr.history import History
from engine.mccfr.infoset import InfoSet
from engine.mccfr.infoset_tracker import InfoSetTracker

Player = NewType('Player', int)


class CFR:
    count = 0
    info_sets: Dict[str, InfoSet]

    def __init__(self, *, create_new_history: Callable[[], History],
                 epochs: int,
                 n_players: int = 2):
        self.n_players = n_players
        self.epochs = epochs
        self.create_new_history = create_new_history

        self.info_sets = {}

        self.tracker = InfoSetTracker()
        self.count = 0

    def _get_info_set(self, h: History):
        print('getting infoset key')
        info_set_key = h.info_set_key()
        if info_set_key not in self.info_sets:
            self.info_sets[info_set_key] = h.new_info_set()
        return self.info_sets[info_set_key]

    def walk_tree(self, h: History, i: Player, pi_i: float, pi_neg_i: float) -> float:
        self.count += 1
        if self.count > 10:
            print('Finishing')
            return 0
        print('Count ', self.count)
        if h.is_terminal():
            print('final leaf')
            return h.terminal_utility(i)

        I = self._get_info_set(h)
        v = 0
        va = {}

        for a in I.actions():
            # insert some logic to skip action, like if meld... just draw discard and skip the other hidden
            if a == 'h':
                # Drawing from hidden pile
                print(i, ' Picking from hidden')
                print('Player that will player: ', h.player())
                history_h = h.draw_from_hidden()
                print('Player that is on history_h: ', history_h.player())
                if i == h.player():
                    va[a] = self.walk_tree(history_h, i, pi_i * I.strategy[a], pi_neg_i)
                else:
                    va[a] = self.walk_tree(history_h, i, pi_i, pi_neg_i * I.strategy[a])
            else:
                # Drawing from discard pile
                print(i, ' Picking from discard')
                print('Player that will player: ', h.player())
                history_d = h.draw_from_discard()
                print('Player that is on history_d: ', history_d.player())

                if i == h.player():
                    va[a] = self.walk_tree(history_d, i, pi_i * I.strategy[a], pi_neg_i)
                else:
                    va[a] = self.walk_tree(history_d, i, pi_i, pi_neg_i * I.strategy[a])

            v = v + I.strategy[a] * va[a]

        if h.player() == i:
            for a in I.actions():
                I.cumulative_strategy[a] = I.cumulative_strategy[a] + pi_i * I.strategy[a]
                print('Action ', a, ' ', I.cumulative_strategy[a])
            for a in I.actions():
                I.regret[a] += pi_neg_i * (va[a] - v)
                print('Action ', a, ' ', I.cumulative_strategy[a])

            I.calculate_strategy()

        return v

    def iterate(self):
        for t in monit.iterate('Train', self.epochs):
            for i in range(self.n_players):
                self.walk_tree(self.create_new_history(), cast(Player, i), 1, 1)

            tracker.add_global_step()
            self.tracker(self.info_sets)
            tracker.save()

            if (t + 1) % 1_000 == 0:
                experiment.save_checkpoint()

        logger.inspect(self.info_sets)
