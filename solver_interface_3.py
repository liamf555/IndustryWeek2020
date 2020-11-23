from typing import *
import numpy as np
from enum import Enum
import dubins

# Preknown to system.
# Each agent maintains a list of its capabilities. Used to match agents to tasks.
class Capability(Enum):
    SAMPLING = 1
    DISPERSAL = 2
    CONTAINMENT = 3
    VISION = 4
    FLIGHT = 5

# Preknown to system.
class Tasks(Enum):
    INIT = 0
    SAMPLE = 1
    CLEANUP = 2
    CONTAIN = 3
    MAPAREA = 4
    FINISH = 5

"""
Object for each specific agent (i.e. two different UAVs have two different Agent objects).
 o Specifies parameters of the agent (its id, name, speed and turning radius).
 o Maintains a list of its capabilities.
 o Maintains an ordered list of the tasks (Task objects) assigned to it.
 o Maintains a list of coordinates of the agent's movement. This is frames[], and is used
   by the graphics plotting code to plot the path of the agent.
"""
class Agent(object):
    def __init__(self, input_id, input_name, input_speed, input_turning_radius):
        self.id = input_id
        self.name = input_name
        self.speed = input_speed
        self.turning_radius = input_turning_radius
        self.tasks = []     # Ordered list of tasks. Tasks are added in order.
        self.capabilities = set()
        self.frames = []
    
    # Returns a list of coordinates (3-tuples - (x, y, heading angle)) which describe the
    # agent's motion through the environment as it progresses through the tasks.
    # Used in the animation in main.main(). Frames are
    # generated in Agent.generateFramesForGraphics(), which in turn calls the generateFrames()
    # function of each of the agent's Task objects. The number of frames generated depends on
    # the frame_rate parameter.
    def getFrames():
        return self.frames

    def addTask(self, task):
        self.tasks.append(task)

    def addCapability(self, cap:Capability):
        self.capabilities.add(cap)

    # Iterate through sequential tasks and generate paths.
    # Each of an Agent's Tasks has a Path object which stores the path from the agent's previous
    # position (at the end of the previous task) to the position of said task. Once an agent's ordered list of tasks has been
    # constructured, this method iterates through the tasks and calls the generation of their
    # paths.
    def generatePaths(self):
        for task_index in range(len(self.tasks)):
            # TODO / NOTE Assumed starting coordinate of (0,0) and angle of 0 for first task.
            if (task_index == 0):
                start_coords = (0, 0)
                start_angle = 0

            self.tasks[task_index].generatePathTo(start_coords, start_angle, self.turning_radius, self.speed)

            # Starting coords of next task path are finishing coords of this one.
            start_coords = self.tasks[task_index].coords
            start_angle = self.tasks[task_index].end_angle

    # See the comment for Agent.getFrames()
    def generateFramesForGraphics(self, frame_rate):
        for task in self.tasks:
            task.generateFrames(self.speed, frame_rate)
            self.frames = self.frames + task.frames

# There is a Task object for each task assigned to an agent.
# Stores (among other details) task coordinates and approach angle, start and end times,
# duration, frames[] for displaying graphics, Path object for storing path to task, a list of the ids of prerequisite
# tasks (tasks which need to be completed before the task described by the object can begin (*) ),
# and a list of capabilities which the task requires.
# (*) Note: in the current implementation, the prerequisite tasks are all required to be complete
# before the agent even __starts moving__ to the task (as opposed to it travelling to the task
# and then waiting to be given permission to begin). 
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

    # Called by the Agent object which 'owns' this task. See Agent.generatePaths().
    def generatePathTo(self, prev_coords, prev_angle, turning_radius, speed):
        # Path to task.
        self.path = Path(prev_coords, self.coords, prev_angle, self.end_angle, turning_radius, speed)


    def assign_prereq_tasks(self, input_prereq_tasks):
        self.prereq_tasks = input_prereq_tasks

    # Recursive method.
    # Populates start and end times for all tasks in dependency chain.
    # Call this on every Task object (as occurs in BaseSolver.resolveTaskTimingDependencies())
    # to populate the start and end times of all task objects.
    # 
    # Each Task object depends on other tasks being complete - the tasks in its prereq_tasks
    # list. Picture this as a tree structure, where each task is a node and the parents of a
    # node are the task's prerequisite tasks. This method sets the start and end times of any
    # Task. The end time is the start time + time to get to the task (time to traverse the path)
    #  + task duration. The start time of a task is the
    # end time of the 'latest finishing' of all of the tasks on which it depends. If this is
    # not known, a recursive call is made to its dependent tasks to generate their start and
    # end times, etc... Since the initial task is at the bottom of the dependency tree, and 
    # its start and end time is known (0 seconds), this provides the base case of the recursion.
    # TODO I don't really like passing 'tasks' in here.
    def generateTimes(self, tasks):# -> float:
        if (self.end_time != -1):
            return self.end_time
        else:
            self.start_time = max(tasks[prereq].generateTimes(tasks) for prereq in self.prereq_tasks)
            self.end_time = self.start_time + self.path.getTime() + self.duration
        return self.end_time
    
    # Generates a list of frames (3-tuples - (x, y, heading angle)) for this particular Task.
    # These are appended to each other in the Agent object to which this task belongs, to form
    # a set of snapshots in time of the agent's movement. These coordinates and headings are then
    # plotted in main.main() as the GUI animation. Distance = speed * time. In this program,
    # all distances are assumed to be in metres and all times are assumed to be in seconds. The time
    # between frames is 1/frame_rate seconds, and the speed is 'speed' m/s, so the distance between
    # frames is speed/frame_rate metres. In reality, when the task coordinates and durations and 
    # agent speeds and turning radii are specified in main.main(), they may need to adopt a different
    # scale, and the frame_rate or playback speed may need to be adjusted in code (in main.main()), to ensure that the
    # number of frames being generated is not a large computational burden; no changes will be necessary
    # to this function.
    # frame_rate = frames per second.
    def generateFrames(self, speed, frame_rate):
        distance_per_frame = speed / frame_rate     # d = s * t => t = 1 / frame_rate
        # Generate points for path to task. Each point will be a frame.
        self.frames, _ = self.path.path.sample_many(distance_per_frame)
        # Add frames for the duration of the task, where the agent remains at the
        # task coordinates.
        # Is there a more efficient way of doing this?
        for i in range(frame_rate * self.duration):
            self.frames.append(self.coords)


# Every Task object has a Path object (path to the task).
# Stores the path and provides methods for generating it, calculating its length, and
# calculating the amount of time it takes the agent to traverse it.
class Path(object):
    def getTime(self) -> float:
        return self.time

    def __init__(self, input_start_coords, input_end_coords, input_start_angle, input_end_angle, input_turning_radius, input_agent_speed): #input_agent:Agent):
        self.coord_s = input_start_coords
        self.coord_e = input_end_coords
        self.start_angle = input_start_angle
        self.end_angle = input_end_angle
        self.turning_radius = input_turning_radius
        self.agent_speed = input_agent_speed

        self.generatePath()
        self.calculateTime()
        self.calculateDistance()

    # Maybe pass path generation function into this? Modify this function to work on an interface?
    # I.e. there could be a DubinsPath class which implements this interface, and other path generating
    # mechanisms could be wrapped up to satisfy the interface as well. Then generating paths according to
    # different mechanisms is just a matter of plugging in the desired class.
    # At the moment, hardcoded to Dubins.
    def generatePath(self):
        dubins_start_list = list(self.coord_s)
        dubins_start_list.append(self.start_angle)
        dubins_end_list = list(self.coord_e)
        dubins_end_list.append(self.end_angle)
        start_params = tuple(dubins_start_list)
        end_params = tuple(dubins_end_list)
        self.path = dubins.shortest_path(start_params, end_params, self.turning_radius)

    def calculateTime(self):
        self.time = self.path.path_length() / self.agent_speed

    def calculateDistance(self):
        self.path_distance = self.path.path_length()


"""
Base class for the various types of solver (PDDL, GA, ...).
Provides an abstract definition of a solve() method for a solver.
Additionally, it takes a plan, which is a dictionary with the following format
    {agent_id:[(task1, [pre1, pre2, ...], heading angle), (task2, [pre1, pre2], heading angle), ...]}
    where pre1, pre2, ... are the ids of the prerequisite tasks. Task and agent numbers are defined
    in the dictionaries passed into the constructor.
and sets up the Agent, Task and Path objects so that timing dependency and motion planning information
can be incorporated for plan evaluation, and frames can be generated for the GUI animation. This class provides
methods for evaluating the total time taken to execute a plan (simulating the motion of the agents)
and calculating the total distance a plan requires the agents to travel (summed over
all agents). Additional evaluation functions can also be added. The timing
prerequisite dependency information is essential for correctly evaluating the total time taken
to execute a plan.
"""
class BaseSolver(object):

    def __init__(self, agents, tasks):
        self.agents = agents
        self.tasks = tasks

    # Outputs plan (see comment for BaseSolver class).
    # Abstract definition. Needs implementing by solver classes which inherit from BaseSolver.
    def solve(self, **kwargs):  # -> Dict[int, List[Tuple[int, List[int], float]]]:
        return {}
    
    # Takes a plan (output from a solver, see BaseSolver class comment) and sets up the Agent, Task and Path objects so that they
    # are ready for an evaluation of the plan (currently total time and total summed distance are the
    # implemented options) and graphics generation for the GUI animation.
    def setPlan(self, input_plan):
        self.plan = input_plan
        self.setup()

    # See comments for functions called.
    def setup(self):
        self.associate()
        self.setupPaths()
        self.resolveTaskTimingDependencies()
    

    # Iterate through plan. Assign Task objects to the Agent objects performing
    # them. Assign Task objects with their list of prerequisite task ids and their finishing
    # heading angle, both as given in the plan.
    def associate(self):
        # For each agent...
        for agent_id in self.plan.keys():
            # plan[agent_id] has form [(task1, [pre1, pre2, ...], heading angle), (task2, [pre1, pre2], heading angle), ...].
            # 'task' is a tuple of the form (task_id, [prereqs. (= task IDs)], heading angle).
            # For each task...
            for task in self.plan[agent_id]:
                task_id = task[0]
                # Ignore the FINISH task (the last task in the tasks dictionary). It is
                # assigned to an agent by the GA, but causes problems if it is not filtered
                # out. Filter out the INIT task as well.
                if (task_id == (len(self.tasks.keys()) - 1)) or (task_id == 0):
                    continue    # Don't assign to an agent.
                prereqs = task[1]
                angle = task[2]
                task = self.tasks[task_id]
                # Assign identifiers of prerequisite tasks.
                task.assign_prereq_tasks(prereqs)
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

    # Populate the start and end times of each Task object by traversing
    # the 'task dependency tree'. See the comment of Task.generateTimes() for a description.
    def resolveTaskTimingDependencies(self):
        # For each task:
        for agent in self.agents.values():
            for task in agent.tasks:
                task.generateTimes(self.tasks)

    # Objective function.
    # Provides the time taken for a solution.
    # This is the maximum (latest) end time of the last task of any agent.
    def evaluate_time(self) -> float:
        end_times = []
        for agent_id in self.agents.keys():
            if (len(self.agents[agent_id].tasks) > 0):
                agent_end_time = self.agents[agent_id].tasks[-1].end_time
            end_times.append(agent_end_time)
        return max(end_times)

    # Objective function.
    # Sums the total distance that each agent travels.
    # Returns the sum of all of these distances.
    def evaluate_total_distance(self) -> float:
        total_distance = 0
        for agent_id in self.agents.keys():
            for task in self.agents[agent_id].tasks:
                total_distance += task.path.path_distance
        return total_distance
    
    # Generate frames (3-tuples - (x, y, heading angle)) for GUI animation. The number of frames
    # generated depends on the frame_rate parameter. This function
    # calls for each Agent object to generate frames for its movement,
    # which in turn causes all of the agent's Task objects to generate their
    # frames. This method returns a dictionary whose keys are agent ids
    # and whose corresponding values are the Agent objects. Each Agent object's list
    # of frames can be accessed by calling Agent.getFrames() on the
    # returned Agent object.
    # Frame rate parameter = number of frames per second.
    def getGraphics(self, frame_rate) -> Dict[int, Agent]:
        # Keys will be the same as agents param passed into init.
        return_agents = {}
        for agent in self.agents.values():
            agent.generateFramesForGraphics(frame_rate)
            return_agents[agent.id] = agent
        return return_agents



    ### NEEDED FOR SOME SOLVER SUB-CLASSES ###

    def dubins_distance(self, c1, c2, turning_radius=0.5):
        return dubins.shortest_path(c1, c2, turning_radius).path_length()

    def dubins_distance_between_tasks(self, t1, t2, turning_radius=0.5):
        c1 = self.tasks[t1][2]
        c2 = self.tasks[t2][2]
        return self.dubins_distance(c1, c2, turning_radius)

    ########################################