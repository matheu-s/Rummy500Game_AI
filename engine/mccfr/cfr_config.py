from typing import NewType, Dict, List, Callable, cast

from labml.configs import BaseConfigs, option
from engine.mccfr.cfr import CFR
from engine.mccfr.history import History


class CFRConfigs(BaseConfigs):
    """
    ### Configurable CFR module
    """
    create_new_history: Callable[[], History]
    epochs: int = 300
    cfr: CFR = 'simple_cfr'


@option(CFRConfigs.cfr)
def simple_cfr(c: CFRConfigs):
    """
    Initialize **CFR** algorithm
    """
    return CFR(create_new_history=c.create_new_history,
               epochs=c.epochs)
