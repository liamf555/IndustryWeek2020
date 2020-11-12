# # import dubins
# # import math

# # q0 = (0.0, 0.0, math.pi/4)
# # q1 = (-4.0, 4.0, -math.pi)
# # turning_radius = 1.0
# # step_size = 0.5

# # qs, _ = dubins.path_sample(q0, q1, turning_radius, step_size)
# # print(qs)

# import numpy as np
# from scipy.spatial.distance import pdist, squareform

# import matplotlib.pyplot as plt
# import scipy.integrate as integrate
# import matplotlib.animation as animation

# class ParticleBox:
#     """Orbits class
    
#     init_state is an [N x 4] array, where N is the number of particles:
#        [[x1, y1, vx1, vy1],
#         [x2, y2, vx2, vy2],
#         ...               ]

#     bounds is the size of the box: [xmin, xmax, ymin, ymax]
#     """
#     def __init__(self,
#                  init_state = [[1, 0, 0, -1],
#                                [-0.5, 0.5, 0.5, 0.5],
#                                [-0.5, -0.5, -0.5, 0.5]],
#                  bounds = [-2, 2, -2, 2],
#                  size = 0.1,
#                  M = 0.05,
#                  G = 9.8):
#         self.init_state = np.asarray(init_state, dtype=float)
#         self.M = M * np.ones(self.init_state.shape[0])
#         self.size = size
#         self.state = self.init_state.copy()
#         self.time_elapsed = 0
#         self.bounds = bounds
#         self.G = G

#     def step(self, dt):
#         """step once by dt seconds"""
#         self.time_elapsed += dt
        
#         # update positions
#         self.state[:, :2] += dt * self.state[:, 2:]

#         # find pairs of particles undergoing a collision
#         D = squareform(pdist(self.state[:, :2]))
#         ind1, ind2 = np.where(D < 2 * self.size)
#         unique = (ind1 < ind2)
#         ind1 = ind1[unique]
#         ind2 = ind2[unique]

#         # update velocities of colliding pairs
#         for i1, i2 in zip(ind1, ind2):
#             # mass
#             m1 = self.M[i1]
#             m2 = self.M[i2]

#             # location vector
#             r1 = self.state[i1, :2]
#             r2 = self.state[i2, :2]

#             # velocity vector
#             v1 = self.state[i1, 2:]
#             v2 = self.state[i2, 2:]

#             # relative location & velocity vectors
#             r_rel = r1 - r2
#             v_rel = v1 - v2

#             # momentum vector of the center of mass
#             v_cm = (m1 * v1 + m2 * v2) / (m1 + m2)

#             # collisions of spheres reflect v_rel over r_rel
#             rr_rel = np.dot(r_rel, r_rel)
#             vr_rel = np.dot(v_rel, r_rel)
#             v_rel = 2 * r_rel * vr_rel / rr_rel - v_rel

#             # assign new velocities
#             self.state[i1, 2:] = v_cm + v_rel * m2 / (m1 + m2)
#             self.state[i2, 2:] = v_cm - v_rel * m1 / (m1 + m2) 

#         # check for crossing boundary
#         crossed_x1 = (self.state[:, 0] < self.bounds[0] + self.size)
#         crossed_x2 = (self.state[:, 0] > self.bounds[1] - self.size)
#         crossed_y1 = (self.state[:, 1] < self.bounds[2] + self.size)
#         crossed_y2 = (self.state[:, 1] > self.bounds[3] - self.size)

#         self.state[crossed_x1, 0] = self.bounds[0] + self.size
#         self.state[crossed_x2, 0] = self.bounds[1] - self.size

#         self.state[crossed_y1, 1] = self.bounds[2] + self.size
#         self.state[crossed_y2, 1] = self.bounds[3] - self.size

#         self.state[crossed_x1 | crossed_x2, 2] *= -1
#         self.state[crossed_y1 | crossed_y2, 3] *= -1

#         # add gravity
#         self.state[:, 3] -= self.M * self.G * dt


# #------------------------------------------------------------
# # set up initial state
# np.random.seed(0)
# init_state = -0.5 + np.random.random((50, 4))
# init_state[:, :2] *= 3.9

# box = ParticleBox(init_state, size=0.04)
# dt = 1. / 30 # 30fps


# #------------------------------------------------------------
# # set up figure and animation
# fig = plt.figure()
# fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
# ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
#                      xlim=(-3.2, 3.2), ylim=(-2.4, 2.4))

# # particles holds the locations of the particles
# particles, = ax.plot([], [], 'bo', ms=6)

# # rect is the box edge
# rect = plt.Rectangle(box.bounds[::2],
#                      box.bounds[1] - box.bounds[0],
#                      box.bounds[3] - box.bounds[2],
#                      ec='none', lw=2, fc='none')
# ax.add_patch(rect)

# def init():
#     """initialize animation"""
#     global box, rect
#     particles.set_data([], [])
#     rect.set_edgecolor('none')
#     return particles, rect

# def animate(i):
#     """perform animation step"""
#     global box, rect, dt, ax, fig
#     box.step(dt)

#     ms = int(fig.dpi * 2 * box.size * fig.get_figwidth()
#              / np.diff(ax.get_xbound())[0])
    
#     # update pieces of the animation
#     rect.set_edgecolor('k')
#     particles.set_data(box.state[:, 0], box.state[:, 1])
#     particles.set_markersize(ms)
#     return particles, rect

# ani = animation.FuncAnimation(fig, animate, frames=600,
#                               interval=10, blit=True, init_func=init)


# # save the animation as an mp4.  This requires ffmpeg or mencoder to be
# # installed.  The extra_args ensure that the x264 codec is used, so that
# # the video can be embedded in html5.  You may need to adjust this for
# # your system: for more information, see
# # http://matplotlib.sourceforge.net/api/animation_api.html
# #ani.save('particle_box.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

# plt.show()




# # class Vehicle(object):

# #     def __init__(self, init_state = (0,0,0), max_vel = 1):
# #         self.init_state = init_state
# #         self.max_vel = max_vel
# #         self.time_elapsed = 0

# #     def step(self, dt):

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



