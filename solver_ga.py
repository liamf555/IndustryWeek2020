from solver_interface import BaseSolver, Capability, Task
import requests, sys
import multiprocessing as mp
import os
import random
from typing import *
from pprint import pprint
import numpy as np
from deap import algorithms, base, creator, tools

creator.create("SingleObjectiveFitness", base.Fitness, weights=(1.0,)) # Maximise Probability Of Completion
creator.create("SingleObjectiveIndividual", _PathChromosome, fitness=creator.SingleObjectiveFitness)

class Chromosome(object):
    pass
