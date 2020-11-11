from solver_interface import BaseSolver, Capability
import requests, sys
import os
from typing import *
from pprint import pprint

class PDDLSolver(BaseSolver):

    def __init__(self,
        agents:List[Tuple[int, List[Capability]]],
        tasks:List[Tuple[int, Tuple[float, float], List[Capability]]],
        **kwargs):
        self.agents = agents
        self.tasks = tasks


    def solve(self, **kwargs) -> Dict[int, List[Tuple[int, float]]]:
        serialize_bin = kwargs.get('serialize_bin', os.path.join('..', 'universal-pddl-parser-multiagent', 'examples', 'serialize', 'serialize.bin'))
        domain_file = kwargs.get('domain_file', os.path.join('pddl', 'domain.pddl'))
        problem_file = kwargs.get('problem_file', os.path.join('pddl', 'pb.pddl'))
        plan = self.compile_and_solver_ma_pddl(serialize_bin, domain_file, problem_file)

        return plan


    def compile_and_solver_ma_pddl(self, serialize_bin, domain_file, problem_file):
        out_domain_file = os.path.join('pddl', 'cl-domain.pddl')
        out_problem_file = os.path.join('pddl', 'cl-pb.pddl')

        # os.system(f'{serialize_bin} {domain_file} {problem_file} > {out_domain_file} 2> {out_problem_file}')

        return self.request_solver_planning(out_domain_file, out_problem_file)

    def request_solver_planning(self, domain_file, problem_file):
        data = {
            'domain': open(domain_file, 'r').read(),
            'problem': open(problem_file, 'r').read()
        }
        resp = requests.post('http://solver.planning.domains/solve',
                     verify=False, json=data).json()

        with open(os.path.join('pddl', 'solver_response_plan'), 'w') as f:
            f.write('\n'.join([act['name'] for act in resp['result']['plan']]))

        result = resp['result']
        if not result['parse_status'] == 'ok':
            print('SOLVER FAILED')
            return {}
        else:
            resplenght = result['length']
            print(f'Found solution of length {resplenght}')
            plan = result['plan']
            return self.parse_pddl_plan(plan)

    def parse_pddl_plan(self, plank):
        agent2num = {'uav': 0, 'submersible': 1, 'boat':2}
        task2num = {'task_init': 0, 'task_maparea': 1, 'task_sample':2, 'task_containment':3, 'task_cleanup': 4, 'task_finish':5}
        plan = {0: [], 1:[], 2:[]}
        curr_time = 0
        for i, p in enumerate(plank):
            print(p)
            name = p['name']
            comm = name[1:-1] # remove brackets
            c = comm.split(' ')
            if c[0] == 'do-move-to-task':
                v = c[1]
                t1 = c[2]
                t2 = c[3]
                dist = self.dubins_distance_between_tasks(t1, t2)

            elif c[0] == 'do-do-task':
                v = c[1]
                t = c[2]
                stuff = (task2num[t], 0.0) #need evaluate
                plan[agent2num[v]].append(stuff)
        return plan


if __name__=='__main__':
    pddlsolver = PDDLSolver([], [])
    plan =  pddlsolver.solve()
    pprint(plan)