from typing import *
import numpy as np
from enum import Enum

class Capability(Enum):
    flight=1
    burning=2

class BaseSolver(object):

    def __init__(
        agents:List[Tuple[int, Capability]],
        tasks:List[Tuple[int, Tuple[float, float], Capability]],
        **kwargs):
        pass


    def solve(**kwargs) -> Dict[int, List[Tuple[int, float]]]:
        return {}