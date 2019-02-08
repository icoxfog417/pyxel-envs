import numpy as np
import pyxel


def round_int(value, percent):
    return np.round(value * percent).astype(int)


class Object2D():

    def __init__(self):
        self._x = -1
        self._y = -1

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def reset(self, x, y):
        self._x = x
        self._y = y

    def step(self, time):
        if self._x < 0 or self._y < 0:
            raise Exception("You have to execute reset before step.")

        self.draw()
        self.update(time)
        return self

    def draw(self):
        raise Exception("Sub class have to implement draw.")

    def update(self, time):
        raise Exception("Sub class have to implement update.")


class Fruit(Object2D):

    def __init__(self, size, speed, color):
        super().__init__()
        self.size = size
        self.speed = speed
        self.color = color

    def draw(self):
        pyxel.circ(self._x, self._y, self.size, self.color)

    def update(self, time):
        self._y = self._y + self.speed * time


class Paddle(Object2D):

    def __init__(self, width, height, speed, color):
        super().__init__()
        self.speed = speed
        self.width = width
        self.height = height
        self.color = color
        self._velocity = 0

    def draw(self):
        dx = self.width / 2
        dy = self.height / 2
        pyxel.rect(self.x - dx, self.y - dy,
                   self.x + dx, self.y + dy, self.color)

    def update(self, move):
        self.velocity += move

        self.velocity *= 0.9


class App():

    def __init__(self, width=64, height=64, init_lives=3):
        self.width = width
        self.height = height
        self.fruit_size = round_int(height, 0.06)
        self.fruit_speed = 0.00095 * height

        self.paddle_width = round_int(width * 0.2)
        self.paddle_height = round_int(height, 0.04)
        self.paddle_speed = 0.021 * width

        self._dx = 0.0
        self._time = 0
        self.init_lives = init_lives

    def run(self):
        pyxel.init(self.width, self.height)
        self.init()
        pyxel.run(self.update, self.draw)

    def init(self):
        self.fruit = Fruit(self.fruit_size, self.fruit_speed, 8)
        self.paddle = Paddle(self.paddle_width, self.paddle_height,
                             self.paddle_speed, 15)

    def reset(self):
        self.fruit.reset(40, 40)

    def update(self):
        if self._time == 0:
            self.reset()

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
            self._dx= 1
        elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
            self._dx = -1

        self.fruit.update(self._time)
        self._time += 1

        if self._time % pyxel.height == 0:
            self._time = 0

    def draw(self):
        pyxel.cls(0)
        self.fruit.draw()


App()
