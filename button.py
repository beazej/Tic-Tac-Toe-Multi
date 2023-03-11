from constants import *
import pygame

class Button:
    def __init__(self, x, y, width, height):
        self.color = BGCOLOR
        self.height = height
        self.width = width
        self.x = x
        self.y = y

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width, self.height), 1, 5)

    def write(self, win, string, color):
        font = pygame.font.SysFont("comicsans", self.height)
        text = font.render(string, 1, color)
        text_rect = text.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
        win.blit(text, text_rect)

