from button import Button
from constants import *
import pygame

class SquareButton (Button):
    def __init__(self, i, j, n):
        self.size = (WIDTH - XMARGIN - SIDE_WIDTH)//n
        super().__init__(XMARGIN + i*self.size, YMARGIN + j*self.size, self.size, self.size)
        self.coor = [i, j]
        self.sign = ''

    def border(self, win, color=(0, 0, 0)):
        pygame.draw.rect(win, color, (self.x, self.y, self.size, self.size), BORDER_SIZE)

    def mark(self, win, mark, color):
        super().write(win, mark, color)
        self.sign = mark

    def print(self):
        return str(self.coor[0]).zfill(2) + str(self.coor[1]).zfill(2)


