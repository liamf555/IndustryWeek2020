from solver_interface_3 import Capability, Tasks, Agent, Task, BaseSolver
from solver_ga import GASolver
from solver_pddl import PDDLSolver
from pprint import pprint
from matplotlib import pyplot as plt
from celluloid import Camera
import numpy as np
import math
from matplotlib.path import Path
import matplotlib.patches as patches

def set_up_tasks():
    # id, type, coords, duration
    t0 = Task(0, Tasks.INIT, (0, 0), 0)
    t1= Task(1, Tasks.MAPAREA, (1, 1), 5)
    t1.addCapability(Capability.VISION)
    t1.addCapability(Capability.FLIGHT)
    t2 = Task(2, Tasks.SAMPLE, (2, 3), 10)
    t2.addCapability(Capability.SAMPLING)
    t3 = Task(3, Tasks.CONTAIN, (5, 3),20)
    t3.addCapability(Capability.CONTAINMENT)
    t4 = Task(4, Tasks.CLEANUP, (2, 2), 12)
    t4.addCapability(Capability.DISPERSAL)
    # No longer use finishing task. We don't care whether the agents return to the starting position
    # after they've finished (we don't care how long it takes them to do this or how far they have
    # to travel - this shouln't be part of the optimisation).
    # Note: this means the PDDL problem file no longer needs to contain 'task_finish', nor
    #   (at uav task_finish)
    #   (at submersible task_finish)
    #   (at boat task_finish)
    # as part of the goal definition.
    #t5 = Task(5, Tasks.FINISH, (0, 0), 0)
    ts = [t0, t1, t2, t3, t4]

    # To be hardcoded/populated by mission planning system.
    return { i: t for i, t in enumerate(ts)}

def set_up_agents():
    # id, name, speed, turning radius -- see solver_interface_3.Agent
    a1 = Agent(0, "uav", 3, 2)
    a1.addCapability(Capability.VISION)
    a1.addCapability(Capability.FLIGHT)
    a2 = Agent(1, "boat", 2, 1.5)
    a2.addCapability(Capability.DISPERSAL)
    a2.addCapability(Capability.CONTAINMENT)
    a3 = Agent(2, "submersible", 4, 1)
    a3.addCapability(Capability.VISION)
    a3.addCapability(Capability.SAMPLING)
    ats = [a1, a2, a3]

    # To be hardcoded/populated by mission planning system.
    return { i : t for i, t in enumerate(ats)}

# For testing
def set_up_tasks_2():
    # id, type, coords, duration
    t0 = Task(0, Tasks.INIT, (0, 0), 0)
    t1= Task(1, Tasks.MAPAREA, (1, 1), 5)
    t1.addCapability(Capability.VISION)
    t1.addCapability(Capability.FLIGHT)
    t2 = Task(2, Tasks.SAMPLE, (2, 3), 10)
    t2.addCapability(Capability.SAMPLING)
    t3 = Task(3, Tasks.SAMPLE, (-4,-3), 10)
    t3.addCapability(Capability.SAMPLING)
    t4 = Task(4, Tasks.CONTAIN, (5, 3), 20)
    t4.addCapability(Capability.CONTAINMENT)
    t5 = Task(5, Tasks.CLEANUP, (2, 2), 12)
    t5.addCapability(Capability.DISPERSAL)
    ts = [t0, t1, t2, t3, t4, t5]

    # To be hardcoded/populated by mission planning system.
    return { i: t for i, t in enumerate(ts)}

# For testing
def set_up_agents_2():
    # id, name, speed, turning radius -- see solver_interface_3.Agent
    a1 = Agent(0, "uav", 3, 0.2)
    a1.addCapability(Capability.VISION)
    a1.addCapability(Capability.FLIGHT)
    a2 = Agent(1, "boat", 2, 0.3)
    a2.addCapability(Capability.VISION)
    a2.addCapability(Capability.SAMPLING)
    a2.addCapability(Capability.CONTAINMENT)
    a3 = Agent(2, "submersible", 4, 0.1)
    a3.addCapability(Capability.DISPERSAL)
    ats = [a1, a2, a3]

    # To be hardcoded/populated by mission planning system.
    return { i : t for i, t in enumerate(ats)}

# For testing
def set_up_tasks_3():
    # id, type, coords, duration
    t0 = Task(0, Tasks.INIT, (0, 0), 0)
    t1= Task(1, Tasks.MAPAREA, (1, 1), 1)
    t1.addCapability(Capability.VISION)
    t1.addCapability(Capability.FLIGHT)
    t2 = Task(2, Tasks.SAMPLE, (2, 3), 1)
    t2.addCapability(Capability.SAMPLING)
    t3 = Task(3, Tasks.CONTAIN, (5, 3), 1)
    t3.addCapability(Capability.CONTAINMENT)
    t4 = Task(4, Tasks.CLEANUP, (2, 2), 1)
    t4.addCapability(Capability.DISPERSAL)
    ts = [t0, t1, t2, t3, t4]

    # To be hardcoded/populated by mission planning system.
    return { i: t for i, t in enumerate(ts)}

# For testing
def set_up_agents_3():
    # id, name, speed, turning radius -- see solver_interface_3.Agent
    a1 = Agent(0, "uav", 30, 0.2)
    a1.addCapability(Capability.VISION)
    a1.addCapability(Capability.FLIGHT)
    #a1.addCapability(Capability.SAMPLING)
    a1.addCapability(Capability.DISPERSAL)
    a1.addCapability(Capability.CONTAINMENT)
    a2 = Agent(1, "boat", 0.2, 1.5)
    a2.addCapability(Capability.VISION)
    a2.addCapability(Capability.SAMPLING)
    a3 = Agent(2, "submersible", 0.4, 1)
    a3.addCapability(Capability.DISPERSAL)
    a3.addCapability(Capability.CONTAINMENT)
    ats = [a1, a2, a3]

    # To be hardcoded/populated by mission planning system.
    return { i : t for i, t in enumerate(ats)}

# For testing
def set_up_tasks_4():
    # id, type, coords, duration
    t0 = Task(0, Tasks.INIT, (0, 0), 0)
    t1= Task(1, Tasks.MAPAREA, (1, 1), 0)#5)
    t1.addCapability(Capability.VISION)
    t1.addCapability(Capability.FLIGHT)
    t2 = Task(2, Tasks.SAMPLE, (2, 3), 0)#10)
    t2.addCapability(Capability.SAMPLING)
    t3 = Task(3, Tasks.SAMPLE, (-4,-3), 0)#10)
    t3.addCapability(Capability.SAMPLING)
    t4 = Task(4, Tasks.CONTAIN, (5, 3), 0)#20)
    t4.addCapability(Capability.CONTAINMENT)
    t5 = Task(5, Tasks.CLEANUP, (2, 2), 0)#12)
    t5.addCapability(Capability.DISPERSAL)
    ts = [t0, t1, t2, t3, t4, t5]

    # To be hardcoded/populated by mission planning system.
    return { i: t for i, t in enumerate(ts)}

# For testing  
def set_up_agents_4():
    # id, name, speed, turning radius -- see solver_interface_3.Agent
    a1 = Agent(0, "uav", 1.6, 0.4)
    a1.addCapability(Capability.VISION)
    a1.addCapability(Capability.FLIGHT)
    a1.addCapability(Capability.SAMPLING)
    a2 = Agent(1, "boat", 0.8, 0.6)
    a2.addCapability(Capability.SAMPLING)
    a2.addCapability(Capability.CONTAINMENT)
    a3 = Agent(2, "submersible", 1.2, 0.3)
    a3.addCapability(Capability.DISPERSAL)
    ats = [a1, a2, a3]

    # To be hardcoded/populated by mission planning system.
    return { i : t for i, t in enumerate(ats)}

# For testing
def set_up_tasks_5():
    # id, type, coords, duration
    t0 = Task(0, Tasks.INIT, (0, 0), 0)
    t1= Task(1, Tasks.MAPAREA, (1, 1), 5)
    t1.addCapability(Capability.VISION)
    t1.addCapability(Capability.FLIGHT)
    t2 = Task(2, Tasks.SAMPLE, (2, 3), 10)
    t2.addCapability(Capability.SAMPLING)
    t3 = Task(3, Tasks.SAMPLE, (-4,-3), 10)
    t3.addCapability(Capability.SAMPLING)
    t4 = Task(4, Tasks.CONTAIN, (5, 3), 20)
    t4.addCapability(Capability.CONTAINMENT)
    t5 = Task(5, Tasks.CLEANUP, (2, 2), 12)
    t5.addCapability(Capability.DISPERSAL)
    ts = [t0, t1, t2, t3, t4, t5]

    # To be hardcoded/populated by mission planning system.
    return { i: t for i, t in enumerate(ts)}

# For testing
def set_up_agents_5():
    # id, name, speed, turning radius -- see solver_interface_3.Agent
    a1 = Agent(0, "uav", 3, 0.2)
    a1.addCapability(Capability.VISION)
    a1.addCapability(Capability.FLIGHT)
    a1.addCapability(Capability.SAMPLING)
    a2 = Agent(1, "boat", 2, 0.3)
    a2.addCapability(Capability.VISION)
    a2.addCapability(Capability.SAMPLING)
    a2.addCapability(Capability.CONTAINMENT)
    a3 = Agent(2, "submersible", 4, 0.1)
    a3.addCapability(Capability.DISPERSAL)
    ats = [a1, a2, a3]

    # To be hardcoded/populated by mission planning system.
    return { i : t for i, t in enumerate(ats)}

def main():
    show_gui = True
    framerate = 10
    solver_select = 'pddl' # 'ga' or 'pddl'
    #Testing
    test_scenario = None # None - run normally. Otherwise number of test scenario to be executed. 

    agents = set_up_agents()
    tasks = set_up_tasks()

    # Testing
    if (test_scenario == 1):
        # Test: In the PDDL file, you can only have one task of each type.
        # Testing to see what happens with the GA (shouldn't be a problem).
        agents = set_up_agents_2()
        tasks = set_up_tasks_2()
    elif (test_scenario == 2):
        # Test: see if a fast agent possessing all possible capabilities will be assigned all tasks [expected behaviour].
        # There seem to sometimes be errors in the GUI.
        agents = set_up_agents_3()
        tasks = set_up_tasks_3()
    elif (test_scenario == 3):
        # Test: check that the prerequisite task system is working - that agents are waiting until other agents have finished
        # completing their tasks before carrying out a dependent one.
        agents = set_up_agents_4()
        tasks = set_up_tasks_4()
        dependency_test_plan = {0:[(1, [0], 0), (3, [2], 0)], 1:[(2, [0], 0), (4, [1, 2, 3], 0)], 2:[(5, [4], 0)]}
        bs = BaseSolver(agents, tasks)
        bs.setPlan(dependency_test_plan)
        solver_select = "testing"
    elif (test_scenario == 4):
        # Testing that PDDL solver handles dependencies correctly (i.e. that it generates a plan which correctly encodes the
        # dependencies).
        agents = set_up_agents_5()
        tasks = set_up_tasks_5()

    # There is an error if both of these solver instances/comparison code
    # are active at the same time.
    if (solver_select == 'ga'):
        solver_GA = GASolver(agents, tasks)
        plan_GA = solver_GA.solve()
        solver_GA.setPlan(plan_GA)

        print("GA Plan: " + str(plan_GA))
        print()
        print("Total time: " + str(solver_GA.evaluate_time()))
        print("Total distance: " + str(solver_GA.evaluate_total_distance()))

        bs = solver_GA
    elif (solver_select == 'pddl'):
        solver_PDDL = PDDLSolver(agents, tasks)
        plan_PDDL = solver_PDDL.solve()
        solver_PDDL.setPlan(plan_PDDL)

        print("PDDL Plan: " + str(plan_PDDL))
        print()
        print("Total time: " + str(solver_PDDL.evaluate_time()))
        print("Total distance: " + str(solver_PDDL.evaluate_total_distance()))

        bs = solver_PDDL
    elif (solver_select == "testing"):
        pass
    else:
        print("Set 'solver_select' to either 'ga' or 'pddl'.")
        exit()

    if (show_gui):
        frames = bs.getGraphics(framerate)

        task_coords = [x.coords for x in tasks.values()]

        task_coords = list(zip(*task_coords))

        task_names = [str(x.type).split('.')[1] for x in tasks.values()]


        fig, ax = plt.subplots()
        camera = Camera(fig)

        names = [x.name for x in frames.values()]

        marker_colors = ['r', 'w', 'g']

        aclist = []

        prev_agent_coords = []

        max_num_frames = max([len(frames[i].frames) for i in range(len(frames.values()))])
        print(max_num_frames)

        for i in range(max_num_frames):
            plt.text(0.3, 0.3, f'frame {i}')
            _agent_coords = [
                x.frames[i] if i < len(x.frames) else prev_agent_coords[j]
                for j, x in enumerate(frames.values())]
            aclist.append(_agent_coords)

            agent_coords = list(zip(*_agent_coords))

            #plot trace
            # for a1s, a2s in zip(aclist, aclist[1:]):
            #     # print('--')
            #     # print(a1s, a2s)
            #     for i, (a1, a2) in enumerate(zip(a1s, a2s)): # per agent
            #         # print(i, a1, a2)
            #         plt.plot(
            #             [a2[0], a1[0]],
            #             [a2[1], a1[1]],
            #             '-', c=marker_colors[i])
            if i > 3:
                codes = [Path.LINETO for _ in range(len(aclist)-2)]
                codes = [Path.MOVETO] + codes + [Path.STOP]
                for k in range(len(frames.values())):
                    alist = [ac[k][:2] for ac in aclist]
                    path = Path(np.array(alist), codes)
                    patch = patches.PathPatch(path, lw=2, color = marker_colors[k], fill = False) # colour to lmarker_colour[k]
                    ax.add_patch(patch)


            # print(coords)
            plt.scatter(agent_coords[0], agent_coords[1], c = marker_colors)

            plt.scatter(task_coords[0], task_coords[1], c = 'k')

            for i, txt in enumerate(names):
                plt.annotate(txt, (agent_coords[0][i], agent_coords[1][i]))

            for i, txt in enumerate(task_names):
                plt.annotate(txt, (task_coords[0][i], task_coords[1][i]))



            ax.set_facecolor("xkcd:sky blue")
            # plt.xlim(-1, 1)
            # plt.ylim(-1, 1)
            camera.snap()

            prev_agent_coords = _agent_coords


        interval = (1/framerate) * 1000
        animation = camera.animate(interval=interval)
        plt.show()

        exit()

if __name__=='__main__':
    main()
