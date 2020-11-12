# Preknown to system.
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


class Task(object):
    def __init__(self, input_id, input_type, input_coords, input_duration):
        self.id = input_id
        self.type = input_type
        self.coord = input_coords
        self.duration = input_duration
        self.start_time = -1
        self.end_time = -1

    # Assigns the actual agent object (not just ID).
    def assign_agent(self, agent_id):  
        self.agent = agents[agent_id]

    def assign_prereq_tasks(self, input_prereq_tasks):
        self.prereq_tasks = input_prereq_tasks


class BaseSolver(object):
    def __init__(self):
        pass

    def 