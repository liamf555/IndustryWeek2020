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
tasks = {1:Task(1, Tasks.MAPAREA, (3, 4), 20), 2:Task(2, Tasks.CONTAIN, (10, 9), 100)}
agents = {}

# Will store capabilities etc.
class AgentDefn(object):
    pass

class Agent(AgentDefn):
    def __init__(self, input_id, input_speed, input_turning_radius):
        self.id = input_id
        self.speed = input_speed
        self.turning_radius = input_turning_radius

class Task(object):
    def __init__(self, input_id, input_type, input_coords, input_duration):
        self.id = input_id
        self.type = input_type
        self.coord = input_coords
        self.duration = input_duration

    # Assigns an actual agent object.
    def assign_agent()
class BaseSolver(object):