from engine.mccfr.cfr_config import CFRConfigs
from engine.mccfr.history import History
from labml.configs import option
from labml import experiment
from labml_nn.cfr.infoset_saver import InfoSetSaver


def create_new_history():
    return History()


class Train(CFRConfigs):
    pass


@option(Train.create_new_history)
def _cnh():
    return create_new_history


def main():
    experiment.create(name='Rummy500', writers={'sqlite'})
    conf = Train()
    experiment.configs(conf)
    experiment.add_model_savers({'info_sets': InfoSetSaver(conf.cfr.info_sets)})

    with experiment.start():
        conf.cfr.iterate()


main()
