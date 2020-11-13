from solver_interface_3 import Capability, Tasks, Agent, Task, BaseSolver
from solver_ga import GASolver
from solver_pddl import PDDLSolver
from pprint import pprint
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

    solver_GA = GASolver(agents, tasks)
    plan_GA = solver_GA.solve()

    # solver_PDDL = PDDLSolver(agents, tasks)
    # plan_PDDL = solver_PDDL.solve()

    bs = BaseSolver(agents, tasks)
    bs.setPlan(plan_GA)
    frames = bs.getGraphics(5)

    # print(str(tasks[0].type).split('.'))

    task_coords = [x.coords for x in tasks.values()]

    task_coords = list(zip(*task_coords))

    task_names = [str(x.type).split('.')[1] for x in tasks.values()]

  

    fig, ax = plt.subplots()
    camera = Camera(fig)

    names = [x.name for x in frames.values()]

    marker_colors = ['r', 'w', 'g']



    for i in range(len(frames[0].frames)):

        agent_coords = [x.frames[i] for x in frames.values()]
        
        agent_coords = list(zip(*agent_coords))

        # print(coords)
        plt.scatter(agent_coords[0], agent_coords[1], c = marker_colors)

        plt.scatter(task_coords[0], task_coords[1], c = 'k')

        for i, txt in enumerate(names):
            plt.annotate(txt, (agent_coords[0][i], agent_coords[1][i]))

        for i, txt in enumerate(task_names):
            plt.annotate(txt, (task_coords[0][i], task_coords[1][i]))
    
        ax.set_facecolor("blue")
    # plt.xlim(-1, 1)
    # plt.ylim(-1, 1)
        camera.snap()

    animation = camera.animate(interval=200) 
    plt.show()








    # print(plan_GA)

    # pprint(bs.plan)





 

   



    
    exit()


    # # very basic cricle to show oil
    # circle1 = plt.Circle((0.5, 0.5), 0.2, color='k')

    # 


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