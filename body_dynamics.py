from abc import abstractmethod


class Body:
    def __init__(self, body_status):
        self._body_status = body_status

    @property
    def m(self):
        return self._body_status[0]

    @m.setter
    def m(self, value):
        self._body_status[0] = value

    @property
    def x(self):
        return self._body_status[1]

    @x.setter
    def x(self, value):
        self._body_status[1] = value

    @property
    def y(self):
        return self._body_status[2]

    @y.setter
    def y(self, value):
        self._body_status[2] = value

    @property
    def vx(self):
        return self._body_status[3]

    @vx.setter
    def vx(self, value):
        self._body_status[3] = value

    @property
    def vy(self):
        return self._body_status[4]

    @vy.setter
    def vy(self, value):
        self._body_status[4] = value

    @property
    def Fx(self):
        return self._body_status[5]

    @Fx.setter
    def Fx(self, value):
        self._body_status[5] = value

    @property
    def Fy(self):
        return self._body_status[6]

    @Fy.setter
    def Fy(self, value):
        self._body_status[6] = value


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
            bodies_status[:, 3:5] += (bodies_status[:, 5:6]/bodies_status[:, 0])*self.dt


class LeapFrogPusher(BodyPusher):

    def __init__(self, time_step):
        self.dt = time_step
        self.is_pre_pushed = False

    def _prepush(self, bodies_status):
        bodies_status[:, 3:5] += (bodies_status[:, 5:6] / bodies_status[:, 0]) * (self.dt/2)

    def push(self, bodies_status, n_steps):
        if not self.is_pre_pushed:
            self._prepush(bodies_status)

        for i in range(n_steps):
            bodies_status[:, 1:3] += bodies_status[:, 3:5] * self.dt
            bodies_status[:, 3:5] += (bodies_status[:, 5:6]/bodies_status[:, 0])*self.dt


if __name__ == '__main__':

    import numpy as np

    bodies_status = np.array([[10., 1., 1., 2., 2., 0., 0.], [5., 2., 2., 1., 1., 1., 1.]])

    bodies = [Body(body_status) for body_status in bodies_status]

    pusher = EulerPusher(0.1)

    for i in range(10):
        pusher.push(bodies_status, 1)
