from solver_interface_3 import Capability, Tasks 
from solver_ga import GASolver
from solver_pddl import PDDLSolver
from matplotlib import pyplot as plt
from celluloid import Camera
import numpy as np

def main():
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

    
    solver = GASolver(agents, tasks)
    plan = solver.solve()



    # very basic cricle to show oil 
    circle1 = plt.Circle((0.5, 0.5), 0.2, color='k')

    for i in ( ):
        
    
        plt.scatter( ( ) , ( ) , c = marker_colors)
        

        #bit of code to add names of agent to points
        for i, txt in enumerate( ):
            plt.annotate(txt, (points[0][i], points[1][i]))
        
        #background colour
        ax.set_facecolor("blue")

        #set plot limits if necessary
        plt.xlim(-1, 1)
        plt.ylim(-1, 1)

        #celluloid steps snapshot
        camera.snap()

    #generates animation based on snaps, uses matplotlib.animation.ArtistAnimation underneath
    animation = camera.animate(interval=200) 
    plt.show()



if __name__=='__main__':
    main()