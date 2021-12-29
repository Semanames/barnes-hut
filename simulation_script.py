from math import log

import numpy as np
from matplotlib import pyplot as plt

from algorithm import ForceCalculator
from body import bodies_generator
from body_dynamics import EulerPusher
from tree import Tree

n_parts = 5000
m = np.append(np.array([10]), np.random.uniform(0.01, 0.02, size=n_parts))
x = np.append(np.array([0.0001]), np.random.normal(0, 2, size=n_parts))
y = np.append(np.array([0.0001]), np.random.normal(0, 2, size=n_parts))
vx = np.append(np.array([0.0]), np.zeros(n_parts))
vy = np.append(np.array([0.0]), np.zeros(n_parts))
Fx = np.zeros(n_parts+1)
Fy = np.zeros(n_parts+1)

bodies_status = np.vstack([m, x, y, vx, vy, Fx, Fy]).T
bodies = bodies_generator(bodies_status)
pusher = EulerPusher(1e-3)
fig = plt.figure()

for i in range(1):
    print(i)
    tree = Tree(-10, 10, -10, 10, fig)
    bodies = bodies_generator(bodies_status)
    tree.update(bodies)
    ForceCalculator(tree).calculate_forces(bodies)
    pusher.push(bodies_status, 1)
    bodies_status = bodies_status[(bodies_status[:, 1] > -10)*(bodies_status[:, 1] < 10)*(bodies_status[:, 2] > -10)*(bodies_status[:, 2] < 10)]
    bodies_status[:, 5:7] = 0.0
    if i % 10 == 0:
        for _, body in enumerate(bodies):
            #plt.arrow(body.x, body.y, body.vx*1e-2, body.vy*1e-2)
            plt.scatter(body.x, body.y, s=body.m**0.5, c='black', alpha=0.5)
        plt.axis('equal')
        plt.xlim([-4, 4])
        plt.ylim([-4, 4])
        plt.show()

