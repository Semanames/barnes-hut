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


def bodies_generator(bodies_status):
    return [Body(body_status) for body_status in bodies_status]