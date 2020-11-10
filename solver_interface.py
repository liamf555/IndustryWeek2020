from typing import *
import numpy as np
from enum import Enum
import dubins

class Capability(Enum):
    flight=1
    burning=2

class BaseSolver(object):

    def __init__(self,
        agents:List[Tuple[int, Capability]],
        tasks:List[Tuple[int, Tuple[float, float], Capability]],
        **kwargs):
        self.agents = agents
        self.tasks = tasks


    def solve(self, **kwargs) -> Dict[int, List[Tuple[int, float]]]:
        return {}


    def evaluate(self, plan: Dict[int, List[Tuple[int, float]]]) -> float:
        longestdist = 0.0
        for anum, path in plan.items():
            #find distance of path
            pass

        return longestdist
