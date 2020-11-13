# TODO
#[o]Still need to finish implementing angle system.
# o What are the units/relative speed of speed? At the moment it is just an arbitrary number.
# o Implement Path.calculateTime()
# LIMITATIONS
# o Initial position assumed to be (0,0) for all agents.
# o Initial angle assumed to be 0 for all agents.
# o Assumes fixed travel speed (no acceleration or deceleration).

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
    FINISH = 5


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
        self.capabilities = set()

    def addTask(self, task):
        self.tasks.append(task)

    def addCapability(self, cap:Capability):
        self.capabilities.add(cap)

    # Iterate through sequential tasks and generate paths.
    def generatePaths(self):
        for task_index in range(len(self.tasks)):
            # TODO / NOTE Assumed starting coordinate of (0,0) and angle of 0 for first task.
            if (task_index == 0):
                start_coords = (0, 0)
                start_angle = 0

            self.tasks[task_index].generatePathTo(start_coords, start_angle, self.turning_radius)

            # Starting coords of next task path are finishing coords of this one.
            start_coords = self.tasks[task_index].coords
            start_angle = self.tasks[task_index].end_angle

    def generateFramesForGraphics(self):
        self.frames = []

    # Not needed - tasks are already in order.
    # TODO implement. Sort tasks in order of increasing start time.
    #def timeSortTasks(self):
    #    pass


class Task(object):
    def __init__(self, input_id, input_type, input_coords, input_duration):
        self.id = input_id
        self.type = input_type
        self.coords = input_coords
        self.capabilities = set()

        # Special override for initial task. Need this for the recursion in generateTimes().
        if (self.type == Tasks.INIT):
            self.duration = 0
            self.start_time = 0
            self.end_time = 0
        else:
            self.duration = input_duration
            self.start_time = -1
            self.end_time = -1

    def addCapability(self, cap:Capability):
        self.capabilities.add(cap)

    def set_end_angle(self, angle):
        self.end_angle = angle

    # TODO Do we still need this?
    # Assigns the actual agent object (not just ID).
    #def assign_agent(self, agent_id):
    #    self.agent = agents[agent_id]

    def generatePathTo(self, prev_coords, prev_angle, turning_radius): #agent:Agent):
        # Path to task.
        self.path = Path(prev_coords, self.coords, prev_angle, self.end_angle, turning_radius)


    def assign_prereq_tasks(self, input_prereq_tasks):
        self.prereq_tasks = input_prereq_tasks

    # Recursive method.
    # Populates start and end times for all tasks in dependency chain.
    # Call this on every task object (as occurs in BaseSolver.resolveTaskTimingDependencies())
    # to populate the start and end times of all task objects.
    # TODO I don't really like passing 'tasks' in here.
    def generateTimes(self, tasks):# -> float:
        if (self.end_time != -1):
            return self.end_time
        else:
            # TODO verify that this is correct syntax.
            # TODO I don't really like passing 'tasks' in here.
            self.start_time = max(tasks[prereq].generateTimes(tasks) for prereq in self.prereq_tasks)
            self.end_time = self.start_time + self.path.getTime() + self.duration
        return self.end_time


# Tasks have paths (path to the task)
class Path(object):
    # Ignore these:
    # coord_s - (float, float)
    # coord_e - (float, float)
    # path_points - [(float, float), (float, float), ...]           # List of tuples of coordinates. E.g. could be Dubins path.
    # time - float

    def getTime(self) -> float:
        return self.time

    ### [Old comment] Wants an actual agent object, not the agent ID
    def __init__(self, input_start_coords, input_end_coords, input_start_angle, input_end_angle, input_turning_radius): #input_agent:Agent):
        self.coord_s = input_start_coords
        self.coord_e = input_end_coords
        self.start_angle = input_start_angle
        self.end_angle = input_end_angle
        self.turning_radius = input_turning_radius
        #self.agent = input_agent

        self.generatePath()
        self.calculateTime()
        self.calculateDistance()

    # Maybe pass path generation function into this?
    # At the moment, hardcoded to Dubins.
    def generatePath(self):
        dubins_start_list = list(self.coord_s)
        dubins_start_list.append(self.start_angle)
        dubins_end_list = list(self.coord_e)
        dubins_end_list.append(self.end_angle)
        start_params = tuple(dubins_start_list)
        end_params = tuple(dubins_end_list)
        self.path = dubins.shortest_path(start_params, end_params, self.turning_radius)

    # TODO implement
    def calculateTime(self):
        # This is where we deal with the step size.
        # Choose a step size.
        # Get the distance (d) of each step.
        # Get the number (n) of steps.
        # Then, where our speed is s (need to think about our units for speed):
        # return (n * d) / s

        #step_size = #?
        #path_points = self.path.sample_many(step_size)
        #n = len(path_points) - 1
        #d = ...

        # Random number, just to test overall implementation of code:
        self.time = 10

    def calculateDistance(self):
        self.path_distance = self.path.path_length()




class BaseSolver(object):
    #self.plan

    def __init__(self, agents, tasks):
        self.agents = agents
        self.tasks = tasks

    # Outputs plan.
    # Dictionary of {agent_id:[(task1, [pre1, pre2, ...], heading), (task2, [pre1, pre2], heading), ...]}
    def solve(self, **kwargs):  # -> Dict[int, List[Tuple[int, List[int], float]]]:
        return {}

    # For changing the plan (remember that this is a dictionary of the form
    #   {agent_id:[(task1, [pre1, pre2, ...], heading angle), (task2, [pre1, pre2], heading angle), ...]}
    # where pre1, pre2, ... are task numbers. Task and agent numbers are defined in the dictionaries passed
    # into the constructor.
    # )
    def setPlan(self, input_plan):
        self.plan = input_plan
        self.setup()

    # Get ready for evaluation.
    def setup(self):
        self.associate()
        self.setupPaths()
        self.resolveTaskTimingDependencies()

    # Sets up references between Task and Agent objects.
    # Want to associate Agent object performing task to each Task object.
    # Want to associate Task objects to Agents performing them.
    def associate(self):
        # For each agent...
        for agent_id in self.plan.keys():
            # plan[agent_id] has form [(task1, [pre1, pre2, ...], heading angle), (task2, [pre1, pre2], heading angle), ...].
            # 'task' is a tuple of the form (task_id, [prereqs. (= task IDs)], heading angle).
            # For each task...
            for task in self.plan[agent_id]:
                task_id = task[0]
                prereqs = task[1]
                angle = task[2]
                task = self.tasks[task_id]
                # Assign agent to task
                # TODO is this actually necessary?
                #task.assign_agent(self.agents[agent_id])
                # Assign identifiers of prerequisite tasks.
                task.assign_prereq_tasks(prereqs)
                # TODO was it meant to be *finishing* heading angle?
                # Assign finishing heading angle to task.
                task.set_end_angle(angle)
                # Assign task to agent
                self.agents[agent_id].addTask(task)

    # Build the paths between tasks for each agent.
    def setupPaths(self):
        # For each agent...
        for agent_id in self.agents.keys():
            # Build the paths for each task...
            self.agents[agent_id].generatePaths()

    # TODO put a comment here about what this method does.
    def resolveTaskTimingDependencies(self):
        # For each task:
        for agent in self.agents.values():
            for task in agent.tasks:
                task.generateTimes(self.tasks)

    # Provides the time taken for a solution.
    # This is the maximum (latest) end time of the last task of any agent.
    def evaluate_time(self) -> float:
        end_times = []
        for agent_id in self.agents.keys():
            if (len(self.agents[agent_id].tasks) > 0):
                agent_end_time = self.agents[agent_id].tasks[-1].end_time
            end_times.append(agent_end_time)
        return max(end_times)

    # Sums the total distance that each agent travels.
    # Returns the sum of all of these distances.
    def evaluate_total_distance(self) -> float:
        total_distance = 0
        for agent_id in self.agents.keys():
            for task in self.agents[agent_id].tasks:
                total_distance += task.path_distance
        return total_distance

    # Maybe add a frame rate parameter
    def getGraphics(self) -> Dict[int, Agent]:
        # Keys will be the same as agents param passed into init.
        return_agents = {}
        for agent in self.agents.values():
            agent.generateFramesForGraphics()
            return_agents[agent.id] = agent
        return return_agents



    ### FOR MICKEY ###

    def dubins_distance(self, c1, c2, turning_radius=0.5):
        return dubins.shortest_path(c1, c2, turning_radius).path_length()

    def dubins_distance_between_tasks(self, t1, t2, turning_radius=0.5):
        c1 = self.tasks[t1][2]
        c2 = self.tasks[t2][2]
        return self.dubins_distance(c1, c2, turning_radius)

    ##################