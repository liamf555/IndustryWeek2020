from solver_interface_3 import Capability, Tasks, Agent, Task
from solver_ga import GASolver
from solver_pddl import PDDLSolver
from matplotlib import pyplot as plt
from celluloid import Camera
import numpy as np
import math

def main():
    t0 = Task(0, Tasks.INIT, (0, 0), 0)
    t1= Task(1, Tasks.MAPAREA, (1, 1), 3)
    t1.addCapability(Capability.VISION)
    t1.addCapability(Capability.FLIGHT)
    t2 = Task(2, Tasks.SAMPLE, (2, 3), 20)
    t2.addCapability(Capability.SAMPLING)
    t3 = Task(3, Tasks.CONTAIN, (5, 3), 15)
    t3.addCapability(Capability.CONTAINMENT)
    t4 = Task(4, Tasks.CLEANUP, (2, 2), 9)
    t4.addCapability(Capability.DISPERSAL)
    t5 = Task(5, Tasks.FINISH, (0, 0), 0)
    ts = [t0, t1, t2, t3, t4, t5]

    a1 = Agent(0, "uav", 3, 2)
    a1.addCapability(Capability.VISION)
    a1.addCapability(Capability.FLIGHT)
    a2 = Agent(1, "boat", 2, 3)
    a2.addCapability(Capability.VISION)
    a2.addCapability(Capability.SAMPLING)
    a3 = Agent(2, "submersible", 1, 1)
    a3.addCapability(Capability.DISPERSAL)
    a3.addCapability(Capability.CONTAINMENT)
    ats = [a1, a2, a3]

    # To be hardcoded/populated by mission planning system.
    tasks = { i: t for i, t in enumerate(ts)}
    # To be hardcoded/populated by mission planning system.
    agents = { i : t for i, t in enumerate(ats)}

    solver = GASolver(agents, tasks)
    plan = solver.solve()

    #solver = GASolver(agents, tasks)
    #plan = solver.solve()


    # plan = {
    #         1:[(1, [0], (math.pi / 4)), (3, [0], (math.pi /3))],
    #         # Just [2] - no 0, depends on previous task for agent 2 which it should anyway.
    #         # [] - test case when it doesn't depend on anything -- would this happen as an output?
    #         2:[(2, [0, 3], (-math.pi / 6)), (4, [2], math.pi), (5, [0], (-math.pi / 5))]
    #         }

    # bs = BaseSolver(agents, tasks)
    # bs.setPlan(plan)
    # print(bs.evaluate_time())
    # print(bs.evaluate_total_distance())


    print(plan)
    exit()


    # # very basic cricle to show oil
    # circle1 = plt.Circle((0.5, 0.5), 0.2, color='k')

    # for i in ( ):


    #     plt.scatter( ( ) , ( ) , c = marker_colors)


    #     #bit of code to add names of agent to points
    #     for i, txt in enumerate( ):
    #         plt.annotate(txt, (points[0][i], points[1][i]))

    #     #background colour
    #     ax.set_facecolor("blue")

    #     #set plot limits if necessary
    #     plt.xlim(-1, 1)
    #     plt.ylim(-1, 1)

    #     #celluloid steps snapshot
    #     camera.snap()

    # #generates animation based on snaps, uses matplotlib.animation.ArtistAnimation underneath
    # animation = camera.animate(interval=200)
    # plt.show()



if __name__=='__main__':
    main()