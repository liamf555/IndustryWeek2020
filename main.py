from solver_interface_3 import Capability, Tasks , BaseSolver, Task, Agent
#from solver_ga import GASolver
#from solver_pddl import PDDLSolver
from matplotlib import pyplot as plt
from celluloid import Camera
import numpy as np
import math

def main():
    # To be hardcoded/populated by mission planning system.
    tasks = {
        # NEED THIS INITIAL TASK
        0:Task(0, Tasks.INIT, (0,0), 0),
        1:Task(1, Tasks.MAPAREA, (3, 4), 20),
        2:Task(2, Tasks.CONTAIN, (10, 9), 100),
        3:Task(3, Tasks.SAMPLE, (2, 5), 10),
        4:Task(4, Tasks.MAPAREA, (12, 1), 30),
        5:Task(5, Tasks.CLEANUP, (10, 3), 150)
        }
    # To be hardcoded/populated by mission planning system.
    agents = {
        1:Agent(1, "UAV", 3, 2),
        2:Agent(2, "Ship", 2, 3),
        3:Agent(3, "Sub", 1, 1)
    }

    
    #solver = GASolver(agents, tasks)
    #plan = solver.solve()

    
    plan = {
            1:[(1, [0], (math.pi / 4)), (3, [0], (math.pi /3))],
            # Just [2] - no 0, depends on previous task for agent 2 which it should anyway.
            # [] - test case when it doesn't depend on anything -- would this happen as an output?
            2:[(2, [0, 3], (-math.pi / 6)), (4, [2], math.pi), (5, [0], (-math.pi / 5))]
            }

    bs = BaseSolver(agents, tasks)
    bs.setPlan(plan)
    print(bs.evaluate_time())
    print(bs.evaluate_total_distance())




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