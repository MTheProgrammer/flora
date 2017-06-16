from Pen import Pen
import pygame, sys
import numpy as np

class Pattern:

    def __init__(self):
        self.pen = Pen()
        self.pen.callback = self.refresh
        pygame.init()
        self.size = 1200, 1080
        self.screen = pygame.display.set_mode(self.size)

    def render(self):
        self.screen.fill([25, 23, 28])
        self.pen.get_state().position = [200, 1000]
        self.pen.draw([
                    'F[+F]F[-F]F',
                    'F[+F]F',
                    'F[-F]F',
                ], 5, np.deg2rad(25.7))
        self.pen.get_state().position = [550, 1000]
        self.pen.draw('F[+F]F[-F][F]', 5, np.deg2rad(20))
        self.pen.get_state().position = [850, 1000]
        self.pen.draw('FF-[-F+F+F]+[+F-F-F]', 4, np.deg2rad(22.5))
        pygame.display.flip()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

    def refresh(self, prev_state, state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        pygame.draw.line(self.screen,
                         self.colorize(prev_state, state),
                         tuple(prev_state.position),
                         tuple(state.position))
        #pygame.display.flip()

    def colorize(self, prev_state, state):
        position = state.position
        col_part = [
            self.clamp(255 * np.sin(position[0]/self.size[0]), 0, 255),
            self.clamp(255 * np.cos(position[1]/self.size[1]), 0, 255),
        ]
        return col_part[1], col_part[0], 55

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)
