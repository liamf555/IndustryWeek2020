import matplotlib
from matplotlib import pyplot as plt
from celluloid import Camera
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum
import dubins

fig, ax = plt.subplots()
camera = Camera(fig)

uav = [-1, -1]
ship = [0.5, 0.5]
sub = [0.2, 0.2]
names = ['uav1', 'ship1', 'sub1']

circle1 = plt.Circle((0.5, 0.5), 0.2, color='k')
circle2 = plt.Circle((-1, -1), 0.6, color='green')

points = list(zip(uav, ship, sub))

marker_colors = ['r', 'w', 'k']
# marker_shapes = ['.', '.']

# class Vehicle(Enum):
#     SUB = 1
#     UAV = 2
#     SHIP = 3

# # @dataclass
# # class Agent():
# #     type: Vehicle
# #     coordinates: List[Tuple(float, float)]

# q0 = (0, 0, 0)
# q1 = (1, 1, 3.14)
# x0 = (0.5, 0.5, 0)
# x1= (0, 0, 0)
# turning_radius = 0.1
# step_size = 0.1

# # points1, _ = dubins.path_sample(q0, q1, 0.1, step_size)
# # points2, _ = dubins.path_sample(q0, q1, 0.2, step_size)
# # points3, _ = dubins.path_sample(q0, q1, 0.3, step_size)

# coords_uav = [(np.random.uniform(-1, 1), np.random.uniform(-1, 1), 0)]
# coords_ship = [(np.random.uniform(-1, 1), np.random.uniform(-1, 1), 0)]
# coords_sub = [(np.random.uniform(-1, 1), np.random.uniform(-1, 1), 0)]

# # print(coords_uav)

# start1 = coords_uav[0]
# start2 = coords_ship[0]
# start3 = coords_sub[0]
# # print(start1)

# for i in range(10):

#     print(start1)

#     x = np.random.uniform(-1, 1, 3)
#     y= np.random.uniform(-1, 1, 3)
#     end1 = (x[0], y[0], 0)
#     end2 = (x[1], y[1], 0)
#     end3 = (x[2], y[2], 0)

#     # print(end1)
   
#     points1,_ = dubins.path_sample(start1, end1, 0.1, step_size)
#     points2,_ = dubins.path_sample(start2, end2, 0.2, step_size)
#     points3,_ = dubins.path_sample(start3, end3, 0.3, step_size)


#     for i, x in enumerate(points1):
#         coords_uav.append(x)
#         coords_ship.append(points2[i])
#         coords_sub.append(points3[i])

#     # print(coords_uav)

#     start1 = coords_uav[-1]
#     start2 = coords_ship[-1]
#     start3 = coords_sub[-1]
    
#     # points1.append(points)


# # points2, _ = dubins.path_sample(x0, x1, turning_radius, step_size)

# points1 = [x[0:2] for x in coords_uav]
# points2 = [x[0:2] for x in coords_ship]
# points3 = [x[0:2] for x in coords_sub]

# print(points1)

# print(points1)

for i in range(100):
    ax.add_artist(circle1)
    ax.add_artist(circle2)
    points = [list(x) for x in points]
    # print(coords)
    plt.scatter(points[0], points[1], c = marker_colors)
    # plt.scatter(coords_ship[i][0], coords_ship[i][1])
    for i, txt in enumerate(names):
        plt.annotate(txt, (points[0][i], points[1][i]))
    
    ax.set_facecolor("blue")
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    camera.snap()
    # points[0] = [x + np.random.uniform(-0.1, 0.1) for x in points[0]]
    # points[1] = [y + np.random.uniform(-0.05, 0.05) for y in points[1]]

    # print(points)
    # print(points[0])
    # print(points[0][1])

    points[0][0] += np.random.uniform(-0.01, 0.1)
    points[1][0] += np.random.uniform(-0.01, 0.1)

    

    points[0][1] += np.random.uniform(-0.05, 0.05)
    points[1][1] += np.random.uniform(-0.05, 0.05)

    points[0][2] += np.random.uniform(-0.02, 0.02)
    points[1][2] += np.random.uniform(-0.02, 0.02)


    # points[2] = [z + np.random.uniform(-0.02, 0.02) for z in points[2]]
    
animation = camera.animate(interval=200) 
plt.show()



