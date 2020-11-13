from solver_interface_3 import BaseSolver, Capability, Tasks, Agent
import requests, sys
import multiprocessing as mp
import os
import random
from typing import *
from pprint import pprint
import numpy as np
from deap import algorithms, base, creator, tools
import dubins

from solver_pddl import PDDLSolver

class _Task(object):
    def __init__(self, id:int, locx:float, locy:float, caps:Set[Capability], predecessor:int):
        self.id = id
        self.caps = set(caps)
        self.locx = locx
        self.locy = locy
        self.predecessor = predecessor
        pass

    def get_loc(self):
        return (self.locx, self.locy)

    def get_pred(self):
        return self.predecessor

    def get_capabilities(self):
        return set(self.caps)

    def __repr__(self):
        return f'T{self.id}_{self.locx}_{self.locx}'

class _Agent(object):
    def __init__(self, id:int, caps:List[Capability]):
        self.id = id
        self.caps = caps

    def get_capabilities(self):
        return set(self.caps)

    def __repr__(self):
        return f'A{self.id}'

class Assignment(object):

    def __init__(self, task, agent):
        self.task = task
        self.agent = agent
        self.heading = random.random() * np.pi

    def __repr__(self):
        return f'ASSNT({self.task},{self.agent},{self.heading})'

class Chromosome(object):

    def __init__(self, agents, tasks):
        self.agents = agents
        self.tasks = tasks
        self.generate_initial_assignment()

    def generate_initial_assignment(self):
        # random_task_ids = np.random.permutation(len(tasks))
        # random_agent_assignments = np.random.choice(list(range(len(agents))), size=len(random_task_ids))
        # self.assignments =  [Assignment(tasks[t], agents[a]) for t, a in zip(random_task_ids, random_agent_assignments)]
        self.len = len(self.tasks)
        task_ordering = []
        while len(task_ordering) < self.len:
            # Chose from task not already selected
            diff = set(self.tasks).difference(set(task_ordering))
            random_task = np.random.choice(list(diff))
            rtpred = random_task.get_pred()
            # Check priority constraints
            previous_tasks = [t.id for t in task_ordering]
            if rtpred in previous_tasks or rtpred == -1:
                task_ordering.append(random_task)

        assns = []
        for task in task_ordering: # Assign agents as per function/capability contraints
            task_reqs = task.get_capabilities()
            while True:
                random_agent = np.random.choice(self.agents)
                racaps = random_agent.get_capabilities()
                if len(task_reqs.intersection(racaps)) == len(task_reqs):
                    assns.append(Assignment(task, random_agent))
                    break

        self.assignments = assns

    def get_prev_tasks(self, idx):
        return [assn.task for assn in self.assignments[:idx]]

    def get_assignments(self):
        return self.assignments

    def get_random_assignment(self):
        rn = np.random.randint(0, self.len)
        return rn, self.assignments[rn]

    def set_assignment(self, idx, assigment):
        self.assignments[rn] = assigment

    def get_random_pair_assignment(self, n=2):
        rns = np.random.choice(list(range(self.len)),size=n, replace=False)
        return [(n, self.assignments[n]) for n in rns]

    def set_assignments(self, idx_assignemnts):
        for idx, assn in idx_assignemnts:
            self.set_assignment(idx, assn)

    def to_dict(self):
        agent_dict = {i:[0] for i in [a.id for a in self.agents]}
        for assn in self.assignments:
            task = assn.task
            agent = assn.agent
            tup = (task.id, [task.get_pred()] if task.get_pred()!=-1 else [0], assn.heading)
            agent_dict[agent.id].append(tup)

        return agent_dict

    def __repr__(self):
        return str(self.assignments)

creator.create("SingleObjectiveFitness", base.Fitness, weights=(-1.0,)) # Maximise Probability Of Completion
creator.create("SingleObjectiveIndividual", Chromosome, fitness=creator.SingleObjectiveFitness)

def _generateIndividual(individual_class, agents, tasks):
    return individual_class(agents, tasks)

def _evaluateChromosome(i, tr=0.5):
    # on distance travelled
    dist = 0
    assns = i.get_assignments()
    for a1, a2 in zip(assns, assns[1:]):
        a1x, a1y = a1.task.get_loc()
        a2x, a2y = a2.task.get_loc()
        dist += dubins.shortest_path((a1x, a1y, a1.heading), (a2x, a2y, a2.heading), tr).path_length()
    return dist,

def _crossoverChromosomes(i1, i2):
    return i1, i2


def _mutate_task_exchange(i):
    (c1idx, c1), (c2idx, c2) = i.get_random_pair_assignment()
    prev_tasks = i.get_prev_tasks(c1idx)
    if c2.task.get_pred() in prev_tasks:
        #swap only if the predecessor of the second has already been completed
        i.set_assignments([
            (c1idx, c2), (c2idx, c1)
        ])
    return i,

def _mutate_heading_angle(i):
    idx, assn = i.get_random_assignment()
    assn.heading = random.random() * np.pi
    return i,

def _mutateChromosomes(i):
    if random.random() > 0.5:
        return _mutate_task_exchange(i)
    else:
        return _mutate_heading_angle(i)

def _getIndividualFitness(ind):
    return ind.fitness.values

class GASolver(BaseSolver):

    def __init__(self,
        agents:List[Tuple[int, List[Capability]]],
        tasks:List[Tuple[int, Tuple[float, float], List[Capability]]],
        **kwargs):
        self.agents = agents
        self.tasks = tasks
        self.pool = mp.Pool(processes=mp.cpu_count())

    def solve(self, **kwargs) -> Dict[int, List[Tuple[int, float]]]: #  outputs -  agentid , list task id and time (input of the evaluate function)

        # pddlsolver = PDDLSolver(self.agents, self.tasks)
        # plan = pddlsolver.plan() # Returns Dict[int, List[int, List[int]]], agent to task and predecessor tasks
        plan = {
            0:[(1,[0])],
            1:[(2,[0])],
            2:[(3,[0]),(4,[0,3])]
        }
        print(self.tasks)
        plan_predec = {t.id:-1 for t in self.tasks.values()}
        for p in plan.values():
            for kc, pred in p:
                plan_predec[kc] = max(plan_predec[kc], np.max(pred))

        _agents = [_Agent(i, c.capabilities) for i, c in self.agents.items()]
        # print(_agents)
        # print(plan_predec)
        _tasks = [_Task(t.id, t.coords[0], t.coords[1], t.capabilities, plan_predec[t.id]) for t in self.tasks.values()]
        print(_tasks)

        self.toolbox = base.Toolbox()
        self.toolbox.register("individual", _generateIndividual, creator.SingleObjectiveIndividual, agents=_agents, tasks=_tasks)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.toolbox.register("evaluate", _evaluateChromosome)
        self.toolbox.register("mate", _crossoverChromosomes)
        self.toolbox.register("mutate", _mutateChromosomes)
        self.toolbox.register("select", tools.selTournament, tournsize=5)
        self.toolbox.register("map", self.pool.map)

        self.stats = tools.Statistics(_getIndividualFitness)
        self.stats.register("avg", np.mean)
        self.stats.register("std", np.std)
        self.stats.register("min", np.min)
        self.stats.register("max", np.max)

        hof = self.quickrun(numgen=2, popsize=10, halloffame=1)

        bestout = hof[0].to_dict()

        return bestout

    def quickrun(self, numgen=20, popsize=100, halloffame=1, cxpb=0.5, mutpb=0.2):
        pop = self.toolbox.population(n=popsize)
        hof = tools.HallOfFame(halloffame)
        pop, log = algorithms.eaSimple(pop, self.toolbox, cxpb=0.5, mutpb=0.2, ngen=40, stats=self.stats, halloffame=hof, verbose=True)

        return hof


if __name__=='__main__':
    agents = {0: [Capability.VISION, Capability.FLIGHT], 1:[Capability.VISION, Capability.SAMPLING], 2:[Capability.DISPERSAL, Capability.CONTAINMENT]}
    tasks = [
        [0, Tasks.INIT, (0,0,0), 0, {}],
        [1, Tasks.SAMPLE, (1,1,0), 3, {Capability.SAMPLING}],
        [2, Tasks.CLEANUP, (2,3,0), 10, {Capability.DISPERSAL}],
        [3, Tasks.CONTAIN, (5,3,0), 7, {Capability.CONTAINMENT}],
        [4, Tasks.MAPAREA, (2,2,0), 5, {Capability.VISION, Capability.FLIGHT}],
        [5, Tasks.FINISH, (0,0,0), 0, {}]
    ]

    gasolver = GASolver(agents, tasks)
    plan = gasolver.solve()

    print(plan)
    # Sample ASSNT
    # c = Chromosome(agents, tasks)
    # print(c)