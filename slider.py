import pygame
from button import Button
from constants import *

class Slider:
    def __init__(self, i, value, label, min_value=0, max_value=255, step=2, starty=400, gap=80):
        self.color = tuple([255 if j == i else 0 for j in range(3)])
        self.label = label
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = value
        self.width = (max_value - min_value + 1)*step
        self.thick = 5
        self.tagHeight = 30
        self.tagWidth = 4
        self.x = XMARGIN + 3*FONT_SIZE*len(label)//4
        self.y = starty + i*gap
        self.button_down = Button(XMARGIN + FONT_SIZE, starty + i*gap - 3*gap//4, SLIDER_BTN_SIZE, SLIDER_BTN_SIZE)
        self.button_up = Button(XMARGIN + self.width, starty + i*gap - 3*gap//4, SLIDER_BTN_SIZE, SLIDER_BTN_SIZE)

    def draw(self, win):
        pygame.draw.line(win, (0, 0, 0), (self.x, self.y), (self.x + self.width, self.y), self.thick)
        pygame.draw.rect(win, self.color, (self.x - 1 + self.step*self.value, self.y - self.tagHeight//2, self.tagWidth, self.tagHeight))
        font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        text = font.render(self.label, 1, self.color)
        win.blit(text, (XMARGIN, self.y - 15))
        text = font.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (XMARGIN + self.width//2, self.y - 60))
        self.button_down.draw(win)
        self.button_up.draw(win)
        self.button_down.write(win, '-', self.color)
        self.button_up.write(win, '+', self.color)

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.button_up.click(pos):
            if self.value < self.max_value:
                self.value += 1
                return True
        if self.button_down.click(pos):
            if self.value > self.min_value:
                self.value -= 1
                return True
        elif self.x <= x1 < self.x + self.width and self.y - self.tagHeight//2 <= y1 <= self.y + self.tagHeight//2:
            self.value = (x1 - self.x)//self.step
            return True
        return False

    def print(self):
        return str(self.value).zfill(3)



