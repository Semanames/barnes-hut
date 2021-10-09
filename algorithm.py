from typing import List

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle


class Body:
    def __init__(self, m, x, y, vx, vy):
        self.m = m
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.Fx = 0
        self.Fy = 0


class Tree:

    def __init__(self,
                 x1: float,
                 x2: float,
                 y1: float,
                 y2: float):

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(x1, x2)
        self.ax.set_ylim(y1, y2)
        self.ax.axis('equal')

        self.root_node = Node(x1, x2, y1, y2, self.ax)

    def update(self, bodies: List[Body]):
        for body in bodies:
            self.ax.scatter(body.x, body.y, color='red', alpha=0.9, s=1)
            self.root_node.update(body)


class Node:

    def __init__(self,
                 x1: float,
                 x2: float,
                 y1: float,
                 y2: float,
                 ax):

        self.is_occupied = False
        self.children = []
        self.mass_center_x = 0
        self.mass_center_y = 0
        self.mass = 0
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.center_x = (x1 + x2) / 2
        self.center_y = (y1 + y2) / 2
        self.leaf_body = None
        self.ax = ax
        self.ax.add_patch(Rectangle((x1, y1), x2-x1, y2-y1, edgecolor='black', fc='none'))

    def create_children(self):
        self.children.append(Node(self.x1, self.center_x, self.center_y, self.y2, self.ax))
        self.children.append(Node(self.center_x, self.x2, self.center_y, self.y2, self.ax))
        self.children.append(Node(self.x1, self.center_x, self.y1, self.center_y, self.ax))
        self.children.append(Node(self.center_x, self.x2, self.y1, self.center_y, self.ax))

    def update(self, body: Body):

        if not self.is_occupied:
            self.mass = body.m
            self.mass_center_x = body.x
            self.mass_center_y = body.y
            self.is_occupied = True
            self.leaf_body = body
            return

        else:
            self.mass_center_x = (self.mass_center_x * self.mass + body.x * body.m) / (self.mass + body.m)
            self.mass_center_y = (self.mass_center_y * self.mass + body.y * body.m) / (self.mass + body.m)
            self.mass += body.m

        if not self.children:
            self.create_children()

        for node in self.children:
            if (node.x1 < body.x <= node.x2) and (node.y1 < body.y <= node.y2):
                node.update(body)
            if self.leaf_body and (node.x1 < self.leaf_body.x <= node.x2) and (node.y1 < self.leaf_body.y <= node.y2):
                node.update(self.leaf_body)
                self.leaf_body = None


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
        Fy = F*(ry - Rx)

        return Fx, Fy


if __name__ == '__main__':
    import random
    bodies = [Body(1, random.uniform(0, 2), random.uniform(0, 2), 0, 0) for _ in range(100)]
    tree = Tree(0, 2, 0, 2)
    tree.update(bodies)
    ForceCalculator(tree).calculate_forces(bodies)
    for i, body in enumerate(bodies):
        plt.arrow(body.x, body.y, body.Fx*1e7, body.Fy*1e7)
        plt.scatter(body.x, body.y, color='black')
    plt.show()
