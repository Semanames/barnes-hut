from abc import abstractmethod

from body import Body


class BodyPusher:

    @abstractmethod
    def push(self, *args):
        pass


class EulerPusher(BodyPusher):

    def __init__(self, time_step):
        self.dt = time_step

    def push(self, bodies_status, n_steps):
        for i in range(n_steps):
            bodies_status[:, 1:3] += bodies_status[:, 3:5] * self.dt
            bodies_status[:, 3:5] += (bodies_status[:, 5:7]/bodies_status[:, 0:1])*self.dt


class LeapFrogPusher(BodyPusher):

    def __init__(self, time_step):
        self.dt = time_step
        self.is_pre_pushed = False

    def _prepush(self, bodies_status):
        bodies_status[:, 3:5] += (bodies_status[:, 5:7] / bodies_status[:, 0]) * (self.dt/2)
        self.is_pre_pushed = True

    def push(self, bodies_status, n_steps):
        if not self.is_pre_pushed:
            self._prepush(bodies_status)

        for i in range(n_steps):
            bodies_status[:, 1:3] += bodies_status[:, 3:5] * self.dt
            bodies_status[:, 3:5] += (bodies_status[:, 5:7]/bodies_status[:, 0])*self.dt


if __name__ == '__main__':

    import numpy as np

    bodies_status = np.array([[10., 1., 1., 2., 2., 0., 0.], [5., 2., 2., 1., 1., 1., 1.]])

    bodies = [Body(body_status) for body_status in bodies_status]

    pusher = EulerPusher(0.1)

    for i in range(10):
        pusher.push(bodies_status, 1)
