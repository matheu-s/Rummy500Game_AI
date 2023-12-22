from typing import List, cast, Dict

import numpy as np

from labml import experiment
from labml.configs import option
from labml_nn.cfr import History as _History, InfoSet as _InfoSet, Action, Player
from labml_nn.cfr.infoset_saver import InfoSetSaver
from engine.mccfr.history import History
from engine.mccfr.cfr_config import CFRConfigs


def create_new_history():
    """A function to create an empty history object"""
    return History()


class Configs(CFRConfigs):
    """
    Configurations extends the CFR configurations class
    """
    pass


@option(Configs.create_new_history)
def _cnh():
    """
    Set the `create_new_history` method for Kuhn Poker
    """
    return create_new_history


def main():
    """
    ### Run the experiment
    """

    # Create an experiment, we only write tracking information to `sqlite` to speed things up.
    # Since the algorithm iterates fast and we track data on each iteration, writing to
    # other destinations such as Tensorboard can be relatively time consuming.
    # SQLite is enough for our analytics.
    experiment.create(name='rummy', writers={'sqlite'})
    # Initialize configuration
    conf = Configs()
    # Load configuration
    experiment.configs(conf)
    # Set models for saving
    experiment.add_model_savers({'info_sets': InfoSetSaver(conf.cfr.info_sets)})
    # Start the experiment
    with experiment.start():
        # Start iterating
        conf.cfr.iterate()
