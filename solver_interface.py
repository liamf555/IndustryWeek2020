from typing import *
import numpy as np
from enum import Enum
import dubins

# To do:
# - List capabilities, agents, tasks
# -

#sampling, flight, dispersal, containment, vision

    #task initialisation (where they start), sample, cleanup, maparea, containment, finish (return to start)

class ObjectiveFunctions(Enum):
    TIME = 1
    CUMULATIVE_DIST = 2

class Capability(Enum):
    SAMPLING = 1
    DISPERSAL = 2
    CONTAINMENT = 3
    VISION = 4
    FLIGHT = 5

class Task(Enum):
    SAMPLE = 1
    CLEANUP = 2
    CONTAIN = 3
    MAPAREA = 4

# Required capabilities. Mapping between task and the capabilities required
# to perform it.
req_cap = {
    (Task.SAMPLE, {Capability.SAMPLING}),
    (Task.CLEANUP, {Capability.DISPERSAL}),
    (Task.CONTAIN, {Capability.CONTAINMENT}),
    (Task.MAPAREA, {Capability.VISION, Capability.FLIGHT})
}

# This information comes from the mission planner.
# taskid, task type, coordinates, duration (seconds).
tasks = [
    (1, Task.SAMPLE, (1,1,0), 3),
    (2, Task.CLEANUP, (2,3,0), 10),
    (3, Task.CONTAIN, (5,3,0), 7),
    (4, Task.MAPAREA, (2,2,0), 5)
    ] # Arbirtary values chosen for the co-ordinates currently

class Agent(object):

    # int id
    # int turning_radius
    # int speed
    # List[Capabilities]
    # List[Tuple(float, float)] # List of frames.

    # Agent needs to have an ID, a list of capabilities, and a list of coordinates.
    def __init__(self, id_input:int, speed: int, input_turning_radius:int, input_capabilities:List[Capabilities]):
        self.id = id_input
        self.step_size = 1 / speed
        self.turning_radius = input_turning_radius
        self.coords = [(0,0)]

    def navigate(self, target_coord:Tuple(float, float)):
        start_coord = tuple(list(self.coords[-1]).append(0))
        path = dubins.shortest_path(start_coord, target_coord, turning_radius)
        configurations, _ = path.sample_many(step_size)

        self.coords.append(element[1:2] for element in configurations)

    def wait(self, num_frames:int)
        last_coord = self.coords[-1]
        for i in xrange(num_frames):
            self.coords.append(last_coord)


    def calculate_time(self):
        pass

class BaseSolver(object):

    def __init__(self,
        agents:List[Tuple[int, Set[Capability]]],
        tasks:List[Tuple[int, int, Tuple[float, float]]],
        **kwargs):
        self.agents = agents
        self.tasks = tasks


    def solve(self, **kwargs) -> Dict[int, List[Tuple[int, float]]]: #  outputs -  agentid , list task id and time (input of the evaluate function)
        return {}


    def evaluate(self, plan: Dict[int, List[Tuple[int, float]]]) -> float):  # input -> agent id (int), task id and time index, output - sum of times or sum of distances
        longestdist = 0.0

        # specify the coordinates for the specific tuple
        starting_coordinates = (0,0,0)

        tasks[int - 1]


        for anum, path in plan.items():
            # Generate a sequence of coordinates for each agent.
            # Each agent can be an object, and this list is assigned to them.
            # task, location -- dubins --> next task.

        # For each task:
        #   Attribute to an agent.
        #   Find the Dubins path and turn into a sequence of coordinates
        #   Calculate the timw (this will be the longest time after any sequence of actions).
        #   If we have to stall, this can still be encoded in the sequence.


            #find distance of path
            pass

        return longestdist

    def evaluate(self,plan):
        total_dist = 0.0
        starting_coordinates = (0,0,0)
        for agent in plan:
            task_id= plan[agent][0]
            task_coordinates = tasks[task_id-1][2]

            path = dubins.shortest_path(starting_coordinates,task_coordinates,0.5)
            configurations, _ = path.sample_many(0.1)
            config = np.array(configurations)
            xy = config[:,0:2]
            agent_dist = np.linalg.norm(xy)
            total_dist += agent_dist

        return total_dist

    def dubins_distance(self, c1, c2, turning_radius=0.5):
        return dubins.shortest_path(c1, c2, turning_radius).path_length()

    def dubins_distance_between_tasks(self, t1, t2, turning_radius=0.5):
        c1 = self.tasks[t1][1]
        c2 = self.tasks[t2][1]
        return self.dubins_distance(c1, c2, turning_radius)

    def generate_graphics(self, plan: Dict[int, List[Tuple[int, float]]]) -> float):
        # For each task
