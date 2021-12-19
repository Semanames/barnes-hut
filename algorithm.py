from typing import List

import numpy as np
from matplotlib import pyplot as plt

from body_dynamics import Body
from tree import Node, Tree


class ForceCalculator:

    def __init__(self, tree: Tree, theta: float = 0.5):

        self.tree = tree
        self.theta = theta

    def calculate_forces(self, bodies: List[Body]):
        for body in bodies:
            self.force_consideration(self.tree.root_node, body)

    def force_consideration(self, node: Node, body: Body):

        if node.is_occupied is False:
            return

        if node.leaf_body is body:
            return

        distance = ((node.mass_center_y - body.y) ** 2 + (node.mass_center_x - body.x) ** 2) ** 0.5

        if (node.x2 - node.x1) / distance < self.theta:
            Fx, Fy = self.gravitational_force(node, body)
            body.Fx += Fx
            body.Fy += Fy
            return
        else:
            for children_node in node.children:
                self.force_consideration(children_node, body)

    @staticmethod
    def gravitational_force(node: Node, body: Body):

        G = 6.67e-11

        M = node.mass
        Rx = node.mass_center_x
        Ry = node.mass_center_y

        m = body.m
        rx = body.x
        ry = body.y

        F = -G*M*m/(((Rx - rx)**2 + (Ry - ry)**2)**(3/2))
        Fx = F*(rx - Rx)
        Fy = F*(ry - Ry)

        return Fx, Fy


if __name__ == '__main__':
    import random
    bodies = [Body(np.array([1, random.uniform(0, 2), random.uniform(0, 2), 0, 0, 0, 0])) for _ in range(1000)]
    fig = plt.figure()
    tree = Tree(0, 2, 0, 2)
    tree.update(bodies)
    ForceCalculator(tree).calculate_forces(bodies)
    for i, body in enumerate(bodies):
        plt.arrow(body.x, body.y, body.Fx*1e5, body.Fy*1e5)
    plt.show()
