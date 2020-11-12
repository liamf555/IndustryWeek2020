# TODO
# o Still need to finish implementing angle system.#
# LIMITATIONS
# o Initial position assumed to be (0,0) for all agents.
# o Initial angle assumed to be 0 for all agents.

from typing import *
import numpy as np
from enum import Enum
import dubins

# Preknown to system.
class Capability(Enum):
    SAMPLING = 1
    DISPERSAL = 2
    CONTAINMENT = 3
    VISION = 4
    FLIGHT = 5

class Tasks(Enum):
    INIT = 0
    SAMPLE = 1
    CLEANUP = 2
    CONTAIN = 3
    MAPAREA = 4

# To be hardcoded/populated by mission planning system.
tasks = {
    1:Task(1, Tasks.MAPAREA, (3, 4), 20),
    2:Task(2, Tasks.CONTAIN, (10, 9), 100)
    }
# To be hardcoded/populated by mission planning system.
agents = {
    1:Agent(1, "UAV", 3, 2),
    2:Agent(2, "Ship", 2, 3),
    3:Agent(3, "Sub", 1, 1)
    }

# Will store capabilities etc.
class AgentDefn(object):
    pass

# Contains capabilities, inherited from AgentDefn base class.
# TODO Use this in actual solver? Work out with Mickey if Agent objects or simply IDs are used.
class Agent(AgentDefn):
    def __init__(self, input_id, input_name, input_speed, input_turning_radius):
        self.id = input_id
        self.name = input_name
        self.speed = input_speed
        self.turning_radius = input_turning_radius
        self.tasks = []     # Ordered list of tasks. Tasks are added in order.

    def addTask(self, task):
        self.tasks.append(task)

    # Iterate through sequential tasks and generate paths.
    def generatePaths(self):
        for task_index in xrange(len(self.tasks)):
            # TODO / NOTE Assumed starting coordinate of (0,0) and angle of 0 for first task.
            if (task_index == 0) {
                start_coords = (0, 0)
                start_angle = 0
            }
            self.tasks[task_index].generatePathTo(start_coords, start_angle, self)

            # Starting coords of next task path are finishing coords of this one.
            start_coords = self.tasks[task_index].coords
            start_angle = self.tasks[task_index].end_angle

    # Not needed - tasks are already in order.
    # TODO implement. Sort tasks in order of increasing start time.
    #def timeSortTasks(self):
    #    pass


class Task(object):
    def __init__(self, input_id, input_type, input_coords, input_end_angle, input_duration):
        self.id = input_id
        self.type = input_type
        self.coords = input_coords
        self.end_angle = input_end_angle

        # Special override for initial task. Need this for the recursion in generateTimes().
        if (self.type == Tasks.INIT):
            self.duration = 0
            self.start_time = 0
            self.end_time = 0
        else:
            self.duration = input_duration
            self.start_time = -1
            self.end_time = -1

    # TODO Do we still need this?
    # Assigns the actual agent object (not just ID).
    def assign_agent(self, agent_id):  
        self.agent = agents[agent_id]

    def generatePathTo(self, prev_coords, prev_angle, agent:Agent):
        # Path to task.
        self.path = Path(prev_coords, self.coords, prev_angle, self.end_angle, agent)


    def assign_prereq_tasks(self, input_prereq_tasks):
        self.prereq_tasks = input_prereq_tasks

    def generateTimes(self) -> float:
        self.start_time = max(prereq.generateTimes() for prereq in self.prereq_tasks)
        self.end_time = self.start_time + self.path_time + self.duration

        for prereq_task in self.prereq_tasks:
            if (prereq_task.end_time == -1):    # Task time is yet to be set.
                self.start_time = prereq_task.generateTimes()
            else:   # end time has been found.
                return self.end_time

# Tasks have paths (path to the task)
class Path(object):
    # coord_s - (float, float)
    # coord_e - (float, float)
    # path_points - [(float, float), (float, float), ...]           # List of tuples of coordinates. E.g. could be Dubins path.
    # time - float

    def getTime(self) -> float:
        return self.time

    # Wants an actual agent object, not the agent IS
    def __init__(self, input_start_coords, input_end_coords, input_start_angle, input_end_angle, input_agent:Agent):
        self.coord_s = input_start_coords
        self.coord_e = input_end_coords
        self.start_angle = input_start_angle
        self.end_angle - input_end_angle
        self.agent = input_agent

        self.generatePath()
        self.calculateTime()

    # Maybe pass path generation function into this?
    # At the moment, hardcoded to Dubins.
    def generatePath(self):
        start_params = tuple(list(self.coord_s).append(self.start_angle))
        end_params = tuple(list(self.coord_e).append(self.end_angle))
        self.path = dubins.shortest_path(start_params, end_params, self.agent.turning_radius)

    # TODO implement
    def calculateTime(self):
        # This is where we deal with the step size.
        pass
                


class BaseSolver(object):
    def __init__(self):
        self.plan = {}
        pass

    # Outputs plan.
    # Dictionary of {agent_id:[(task1, [pre1, pre2, ...], heading), (task2, [pre1, pre2], heading), ...]}
    def solve(self, **kwargs) -> Dict[int, List[Tuple[int, List[int], float]]]:
        return {}

    # Sets up references between Task and Agent objects.
    # Want to associate Agent object performing task to each Task object.
    # Want to associate Task objects to Agents performing them.
    def associate(self, plan):
        # For each agent...
        for agent_id in plan.keys():
            # plan[agent_id] has form [(task1, [pre1, pre2, ...], heading), (task2, [pre1, pre2], heading), ...].
            # 'task' is a tuple of the form (task_id, [prereqs. (= task IDs)], heading).
            # For each task...
            for task in plan[agent_id]:
                task_id = task[0]
                prereqs = task[1]
                task = tasks[task_id]
                # Assign agent to task
                task.assign_agent(agents[agent_id])
                task.assign_prereq_tasks(prereqs)
                # Assign task to agent
                agents[agent_id].addTask(task)

    def generateTimes(self):
        # Pseudocode:
        # For each task:
        #   Iterate through the list of prerequisite tasks.

    # Provides the time taken for a solution
    def evaluate_time(self, plan) -> float:
        
        

    def evaluate_total_distance(self):

