from typing import NewType, Dict, List, Callable, cast

from labml import monit, tracker, logger, experiment
from engine.mccfr.history import History
from engine.mccfr.infoset import InfoSet
from engine.mccfr.infoset_tracker import InfoSetTracker


Player = NewType('Player', int)

Action = NewType('Action', str)


class CFR:
    """
    ## Counterfactual Regret Minimization (CFR) Algorithm

    We do chance sampling (**CS**) where all the chance events (nodes) are sampled and
    all other events (nodes) are explored.

    We can ignore the term $q(z)$ since it's the same for all terminal histories
    since we are doing chance sampling and it cancels out when calculating
    strategy (common in numerator and denominator).
    """

    # $\mathcal{I}$ set of all information sets.
    info_sets: Dict[str, InfoSet]

    def __init__(self, *,
                 create_new_history: Callable[[], History],
                 epochs: int,
                 n_players: int = 2):
        """
        * `create_new_history` creates a new empty history
        * `epochs` is the number of iterations to train on $T$
        * `n_players` is the number of players
        """
        self.n_players = n_players
        self.epochs = epochs
        self.create_new_history = create_new_history
        # A dictionary for set of all information sets
        self.info_sets = {}
        # Tracker for analytics
        self.tracker = InfoSetTracker()

    def _get_info_set(self, h: History):
        """
        Returns the information set $I$ of the current player for a given history $h$
        """
        info_set_key = h.info_set_key()
        if info_set_key not in self.info_sets:
            self.info_sets[info_set_key] = h.new_info_set()
        return self.info_sets[info_set_key]

    def walk_tree(self, h: History, i: Player, pi_i: float, pi_neg_i: float) -> float:
        print('This is plauer ', i , ' iterating the tree ', h.history)

        # right after first action after deal
        # if len(h.history) == 1:
        #     print('at this point, cards are the following: ')
        #     print('p0 cards', h.p0_cards)
        #     print('p1 cards', h.p1_cards)

        # If it's a terminal history, return the terminal utility $u_i(h)$.
        if h.is_terminal():
            # print('is terminal, utility is for plauer ', i, ' is ',  h.terminal_utility(i))
            # print('player 0 had ', h.p0_points)
            # print('player 1 had ', h.p1_points)
            return h.terminal_utility(i)
        # If it's a chance event $P(h) = c$ sample a and go to next step.
        elif h.is_chance():
            print('dealing cards')
            h.sample_chance()

        # Get current player's information set for h
        I = self._get_info_set(h)

        # To store utility
        v = 0
        # To store for each action $a \in A(h)$
        va = {}

        # Iterate through all actions
        for a in I.actions():
            print('in action ', a)
            # If the current player is $i$,
            if i == h.player():
                va[a] = self.walk_tree(h + a, i, pi_i * I.strategy[a], pi_neg_i)
            # Otherwise,
            else:
                va[a] = self.walk_tree(h + a, i, pi_i, pi_neg_i * I.strategy[a])
            v = v + I.strategy[a] * va[a]

        # If the current player is $i$,
        # update the cumulative strategies and total regrets
        if h.player() == i:
            for a in I.actions():
                I.cumulative_strategy[a] = I.cumulative_strategy[a] + pi_i * I.strategy[a]
            for a in I.actions():
                I.regret[a] += pi_neg_i * (va[a] - v)

            # Update the strategy
            I.calculate_strategy()

        # Return the expected utility for player $i$,
        # print('utility is: ', v)
        # print('for player ', i)
        # print('when history was  ', h.history)
        # print('utility is: ', v)
        # print('updated ', h.info_set_key())
        return v

    def iterate(self):
        # print('iterating')
        # Loop for `epochs` times
        for t in monit.iterate('Train', self.epochs):
            # Walk tree and update regrets for each player
            for i in range(self.n_players):
                self.walk_tree(self.create_new_history(), cast(Player, i), 1, 1)

            # Track data for analytics
            tracker.add_global_step()
            self.tracker(self.info_sets)
            tracker.save()

            # Save checkpoints every 10 iterations
            if (t + 1) % 50 == 0:
                experiment.save_checkpoint()

        # Print the information sets
        logger.inspect(self.info_sets)
