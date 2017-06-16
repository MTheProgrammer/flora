import copy
import math
from random import randint


class PenState:
    color = [230, 230, 230, 0]
    position = [400, 1000]
    angle = 0
    scale = 10.0


class Pen:
    codes = {
        #'F': 'fwd',
        'F': 'draw',
        'R': 'right',
        'L': 'left',
        '-': 'right',
        '+': 'left',
        '[': 'stash',
        ']': 'pop'
    }

    def __init__(self):
        self.states = []
        self.states.append(PenState())
        self.drawing = True
        self.angle = 0.2
        self.commands = {}
        for code in Pen.codes:
            self.commands[code] = getattr(self, Pen.codes[code])

    def get_state(self):
        return self.states[-1]

    def stash(self):
        state = copy.copy(self.states[-1])
        self.states.append(state)

    def pop(self):
        self.states.pop()

    def turn(self, angle):
        self.get_state().angle += angle

    def left(self):
        self.turn(-self.angle)

    def right(self):
        self.turn(self.angle)

    def fwd(self):
        state = self.get_state()
        prev_state = copy.copy(state)
        theta = state.angle
        cs = math.cos(theta)
        sn = math.sin(theta)

        delta = [0, -state.scale]

        x = delta[0]
        y = delta[1]

        px = x * cs - y * sn + state.position[0]
        py = x * sn + y * cs + state.position[1]
        state.position = [px, py]
        self.after_move(prev_state, state)

    def after_move(self, prev_state, state):
        if self.drawing:
            self.callback(prev_state, state)

    def draw(self, commands, iter, angle):
        self.angle = angle
        if iter == 0:
            self.fwd()
            return

        iter -= 1
        used_commands = commands
        if isinstance(commands, list):
            rand = randint(0, len(commands) - 1)
            used_commands = commands[rand]

        for command in used_commands:
            method = self.commands[command]
            if command == 'F':
                method(commands, iter, angle)
            else:
                method()

