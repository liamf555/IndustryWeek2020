from typing import *
import numpy as np
from enum import Enum
import dubins

# Thinking clearly about data structures.
# Input from PDDL solver will be dictionary - {agent1:[task_id, [pre1, pre2, ...]], agent2:[task_id, [pre1, pre2, ...]]}
# Agent stores an ordered list of tasks = [{coord_s:(x_s, y_s), coord_e:(x_e, y_e), duration:value, precons:[pre1, pre2, ...]}]
# For each task, need to plug in path generation algorithm; calculate path and time.
# Then string together, 'waiting' for dependent tasks.

# Get results of solver: plan
# Method in BaseSolver, just writing here for now.

######################################
# Major limitations:
#  o At the moment, assumes that all tasks take the same amount of time (duration is given in TaskDefinition object). In reality, some e.g. containment operations may take longer than others.

class Capability(Enum):
    SAMPLING = 1
    DISPERSAL = 2
    CONTAINMENT = 3
    VISION = 4
    FLIGHT = 5

class Tasks(Enum):
    SAMPLE = 1
    CLEANUP = 2
    CONTAIN = 3
    MAPAREA = 4

# Dictionary of agents. {agent_id:Agent}
agents = {}

# Dictionary of task definitions. {task_id: TaskDefinition}. TaskDefinition is an object: one object for each task.
class TaskDefinition(object):
   def __init__(self, i_name, i_duration:float, i_caps:List[Capability]):
       self.name = i_name
       self.duration = i_duration
       self.caps = i_caps

task_defs = {
            Tasks.MAPAREA:TaskDefinition("burnoff", 100, [Capability.VISION, Capability.HIGH_SPEED]),
            Tasks.SAMPLE:TaskDefinition("sample", 20, [Capability.SAMPLING])
}

# Maps task IDs to their definitions.
task_map = {
            1:task_defs[Tasks.MAPAREA],
            2:task_defs[Tasks.SAMPLE],
            3:task_defs[Tasks.MAPAREA]
            }  #e.g.

task_instances = []

# Generate Task objects and put them into a list.
def generateTaskList(self, plan: Dict[int, List[Tuple[int, List[int]]]]):
    for agent_id in plan.keys():
        # plan[agent_id] is a list of tasks. Each task is a tuple with (task_id, [prereqs. - task IDs]).
        for task in plan[agent_id]:
            task_num = task[0]
            prereqs = task[1]
            task_instances.append(Task(task_num, agents[agent_id], task_map[task_num].duration, prereqs))
        

# Iterate through tasks, populating times.
def generateTimes():
    for task in self.task_instances:
        for prereq_task in task.


class Task(object):
    def __init__(self, input_task_id:int, assigned_agent:Agent, task_duration:float, input_prereq_tasks:List[Task]):
        self.task_id = input_task_id
        self.agent = assigned_agent  # Reference to assigned agent object.
        self.duration = task_duration
        self.prereq_tasks = input_prereq_tasks
        self.path = Path(task_instances[)
        self.start_time = -1
        self.end_time = -1
    

class Path(object):
    #coord_s = (0, 0)
    #coord_e = (0, 0)
    #path = []           # List of tuples of coordinates. E.g. could be Dubins path.
    #time = #

    def __init__(self, input_s_coords, input_e_coords, assigned_agent:Agent):
        self.coord_s = input_s_coords
        self.coord_e = input_e_coords
        self.agent = assigned_agent

        self.generatePath()
        self.calculateTime()

    # Maybe pass path generation function into this?
    # At the moment, hardcoded to Dubins.
    def generatePath():
        path = dubins.shortest_path(self.coords_s, self.coords_e, self.agent.turning_radius)

    # TODO implement
    def calculateTime():
        # This is where we deal with the step size.
        pass


#sampling, flight, dispersal, containment, vision

    #task initialisation (where they start), sample, cleanup, maparea, containment, finish (return to start)

##################################### <DON'T NEED ANY OF THIS FOR DEMO> ################################
class ObjectiveFunctions(Enum):
    TIME = 1
    CUMULATIVE_DIST = 2



# Required capabilities. Mapping between task and the capabilities required
# to perform it.
req_cap = {
    Task.SAMPLE:{Capability.SAMPLING},
    Task.CLEANUP:{Capability.DISPERSAL},
    Task.CONTAIN:{Capability.CONTAINMENT},
    Task.MAPAREA:{Capability.VISION, Capability.FLIGHT}
}

# This information comes from the mission planner.
# taskid, task type, coordinates, duration (seconds).
tasks = [
    (1, Task.SAMPLE, (1,1), 30),
    (2, Task.CLEANUP, (2,3), 100),
    (3, Task.CONTAIN, (5,3), 70),
    (4, Task.MAPAREA, (2,2), 50)
    ] # Arbirtary values chosen for the co-ordinates currently

##################################### </DON'T NEED ANY OF THIS FOR DEMO> ################################

class Agent(object):
    
    # int id
    # int turning_radius
    # int speed
    # List[Capabilities]
    # List[Tuple(float, float)] # List of frames.

    # Agent needs to have an ID, a list of capabilities, and a list of coordinates.
    def __init__(self, id_input:int, speed:int, input_turning_radius:int, input_capabilities:List[Capabilities]):
        self.id = id_input
        self.step_size = 1 / speed
        self.turning_radius = input_turning_radius
        self.coords = [(0,0)]

    def navigate(self, target_coord:Tuple(float, float)):
        #self.coords[-1] is a tuple - (x,y). start_coord will be (x, y, 0).
        start_coord = tuple(list(self.coords[-1]).append(0))
        path = dubins.shortest_path(start_coord, target_coord, turning_radius)
        configurations, _ = path.sample_many(step_size)

        self.coords.append(element[1:2] for element in configurations)

    def wait(self, num_frames:int):
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
        # Agents:
        # 0: UAV (fastest)
        # 1: Sub (slowest)
        # 2: Boat
        self.agents = {
            0:Agent(0, 3, 2, None),
            1:Agent(1, 1, 1, None),
            2:Agent(2, 2, 3, None)
            }
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

    #agent, [(task, time), ]
    plan = {1:[(1, 40), (3, 55)], 2:[(2, 20), (4, 10)]}

    '''
    def evaluate(self,plan):
        total_dist = 0.0
        starting_coordinates = (0,0,0)
        for agent in plan.keys():
            for task in plan[agent]:
                task_id= task[0]
                task_coordinates = tasks[task_id-1][2]

                path = dubins.shortest_path(starting_coordinates,task_coordinates,0.5)
                configura
                config = np.array(configurations)
                xy = config[:,0:2]
                agent_dist = np.linalg.norm(xy)
                total_dist += agent_dist
    
        return total_dist
    '''
    def evaluate(self,plan):
        total_dist = 0.0
        starting_coordinates = (0,0,0)
        for agent in plan.keys()
            for task in plan[agent]:
                task_id= task[0]
                task_coordinates = tasks[task_id-1][2]
                path = dubins.shortest_path(starting_coordinates,task_coordinates,self.agents[agent].turning_radius)
                agent_dist = path.path_length()
                #configurations, _ = path.sample_many(0.1)
                #config = np.array(configurations)
                #xy = config[:,0:2]
                total_dist += agent_dist
        return total_dist

    def dubins_distance(self, c1, c2, turning_radius=0.5):
        return dubins.shortest_path(c1, c2, turning_radius).path_length()

    def dubins_distance_between_tasks(self, t1, t2, turning_radius=0.5):
        c1 = self.tasks[t1][2]
        c2 = self.tasks[t2][2]
        return self.dubins_distance(c1, c2, turning_radius)

    # Need a dictionary: {agent_id:agent}
    # {agent_id:[(task, time), (task, time), ...]}
    def generate_graphics(self, plan: Dict[int, List[Tuple[int, float]]]):
        # For each task
        # 'agent' is the agent number
        for agent in plan.keys():
            for task in plan[agent]     # For each task that the agent needs to do
                task_id= task[0]
                task_coordinates = tasks[task_id-1][2]
                task_duration = tasks[task_id-1][3]

                agents[agent].navigate(task_coordinates)
                agents[agent].wait(task_duration)