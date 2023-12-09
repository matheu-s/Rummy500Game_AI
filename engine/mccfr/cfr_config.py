from labml.configs import BaseConfigs, option
from typing import Callable
from engine.mccfr.history import History
from engine.mccfr.cfr import CFR


class CFRConfigs(BaseConfigs):
    create_new_history: Callable[[], History]
    epochs: int = 1
    cfr: CFR = 'simple_cfr'

@option(CFRConfigs.cfr)
def simple_cfr(c: CFRConfigs):
    return CFR(create_new_history=c.create_new_history, epochs=c.epochs)