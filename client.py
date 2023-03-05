import pygame
from network import Network
import pickle
from constants import *

pygame.font.init()

WIDTH = 850
HEIGHT = 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")
RUN = True
FONT = pygame.font.SysFont("comicsans", 50)

class Button:
    def __init__(self, i, j, n):
        self.n = n
        self.color = BGCOLOR
        self.size = (WIDTH - 250)//self.n
        self.x = 50 + i*self.size
        self.y = 100 + j*self.size
        self.coor = [i, j]
        self.sign = ''

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.size, self.size), 1, 5)

    def border(self, win, color=(0, 0, 0)):
        pygame.draw.rect(win, color, (self.x, self.y, self.size, self.size), 5)

    def mark(self, win, mark, color):
        font = pygame.font.SysFont("comicsans", self.size)
        text = font.render(mark, 1, color)
        text_rect = text.get_rect(center=(self.x + self.size//2, self.y + self.size//2))
        #win.blit(text, (self.x + self.size//4, self.y + self.size//4))
        win.blit(text, text_rect)
        self.sign = mark

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.size and self.y <= y1 <= self.y + self.size:
            return True
        else:
            return False

    def print(self):
        return str(self.coor[0]).zfill(2) + str(self.coor[1]).zfill(2)

class Slider:
    def __init__(self, i, value, letter):
        self.buttonDown = Button(2, 2*i + 6, 15)
        self.buttonUp = Button(12, 2*i + 6, 15)
        self.color = tuple([255 if j == i else 0 for j in range(3)])
        self.letter = letter
        self.value = value
        self.width = 512
        self.thick = 5
        self.tagHeight = 30
        self.tagWidth = 4
        self.x = 88
        self.y = 400 + i*80

    def draw(self, win):
        pygame.draw.line(win, (0, 0, 0), (self.x, self.y), (self.x + self.width, self.y), self.thick)
        pygame.draw.rect(win, self.color, (self.x - 1 + 2*self.value, self.y - self.tagHeight//2, self.tagWidth, self.tagHeight))
        text = FONT.render(self.letter, 1, self.color)
        win.blit(text, (50, self.y - 15))
        text = FONT.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (300, self.y - 60))
        self.buttonDown.draw(win)
        self.buttonUp.draw(win)
        self.buttonDown.mark(win, '-', self.color)
        self.buttonUp.mark(win, '+', self.color)

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.buttonUp.click(pos):
            if self.value < 255:
                self.value += 1
                return True
        if self.buttonDown.click(pos):
            if self.value > 0:
                self.value -= 1
                return True
        elif self.x <= x1 < self.x + self.width and self.y - self.tagHeight//2 <= y1 <= self.y + self.tagHeight//2:
            self.value = (x1 - self.x)//2
            return True
        return False

    def print(self):
        return str(self.value).zfill(3)

def makeBoard(win, p, results):
    win.fill(BGCOLOR)
    text = FONT.render("Jesteś graczem " + str(p), 1, COMCOLOR)
    win.blit(text, (50, 0))
    btns = [Button(i, j, 3) for i in range (3) for j in range(3)]

    for btn in btns:
        btn.draw(win)
    text = FONT.render("Wygrane: " + results[0] + " Przegrane: " + results[1] + " Remis: " + results[2], 1, COMCOLOR)
    win.blit(text, (50, 750))
    return btns

def drawSelectMark(win, color):
    btns = [Button(i, j, 6) for i in range(6) for j in range(2)]
    for i in range(len(MARKS)):
        btns[i].draw(win)
        btns[i].mark(win, MARKS[i], color)
    return btns

def drawSelectColor(win, rgb):
    colors = [(255, 0 ,0), (0, 255, 0), (0, 0, 255)]
    L = 'RGB'
    colorBtns = [[Button(10*i + 2, 2*j + 6, 15) for i in range(2)] for j in range(3)]
    for i in range(3):
        pygame.draw.line(win, (0, 0, 0), (88, 400 + 80*i), (600, 400 + 80*i), 5)
        pygame.draw.rect(win, colors[i], (87 + 2*rgb[i], 385 + 80*i, 4, 30))
        text = FONT.render(L[i], 1, colors[i])
        win.blit(text, (50, 385 + 80*i))
        text = FONT.render(str(rgb[i]), 1, (0, 0, 0))
        win.blit(text, (300, 340 + 80*i))
        colorBtns[i][0].draw(win)
        colorBtns[i][0].mark(win, '<', colors[i])
        colorBtns[i][1].draw(win)
        colorBtns[i][1].mark(win, '>', colors[i])
    return colorBtns


def drawSidebar(win, game, player=-1):
    btns = [[Button(13 + i, j, 12) for i in range(2)] for j in range(game.players)]
    for i in range(game.players):
        btns[i][0].draw(win)
        btns[i][1].draw(win)
        btns[i][0].mark(win, str(i), game.colors[i])
        btns[i][1].mark(win, game.marks[i], game.colors[i])
        if player == -1 and  game.choose[i]:
                btns[i][1].border(win, COMCOLOR)
    if player != -1:
        btns[player][1].border(win, ACOLOR)
        
    
def main():
    run = True
    global RUN
    clock = pygame.time.Clock()
    n = Network()
    started = False
    moved = False
    finished = False
    reset = False
    try:
        player = int(n.getP())
    except:
        run = False
    choosing = True
    print("You are player", player)
    btns = []
    yesBtn = Button(10, 12, 12)
    noBtn = Button(11, 12, 12)
    okBtn = Button(11, 10, 12)
    currentChoice = player
    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Nie znaleziono gry")
            break
        if not game.connected():
            win.fill(BGCOLOR)
            font = pygame.font.SysFont("comicsans", 80)
            text = font.render("Czekasz na gracza...", 1, (255,0,0), True)
            win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    RUN = False
                    pygame.quit()
        elif choosing:
            win.fill(BGCOLOR)
            text = FONT.render("Jesteś graczem " + str(player), 1, COMCOLOR)
            win.blit(text, (50, 0))
            text = FONT.render("Wybierz symbol", 1, COMCOLOR)
            win.blit(text, (50, 50))
            pColor = game.colors[player]
            selectBtns = drawSelectMark(win, pColor)
            sliders = [Slider(i, pColor[i], 'RGB'[i]) for i in range(3)]
            for slider in sliders:
                slider.draw(win)
            text = FONT.render("Czy potwierdzasz wybór?", 1, COMCOLOR)
            win.blit(text, (50, 610))
            okBtn.draw(win)
            okBtn.mark(win, 'T', (0, 255, 0))
            selectBtns[currentChoice].border(win, ACOLOR)
            drawSidebar(win, game)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    RUN = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btn in selectBtns:
                        if btn.click(pos):
                            n.send('M' + btn.sign)
                            oldChoice = currentChoice
                            currentChoice = 2*btn.coor[0] + btn.coor[1]
                    for slider in sliders:
                        if slider.click(pos):
                            n.send('C' + sliders[0].print() + sliders[1].print() + sliders[2].print())
                    if okBtn.click(pos):
                        choosing = False
                        n.send("choosed")
        elif not game.choosed():
            win.fill(BGCOLOR)
            text = FONT.render("Jesteś graczem " + str(player), 1, COMCOLOR)
            win.blit(text, (50, 0))
            text = FONT.render("Czekasz na innych graczy", 1, COMCOLOR, BGCOLOR)
            win.blit(text, (50, 250))
            text = FONT.render("Chcesz wrócić do wybierania?", 1, COMCOLOR)
            win.blit(text, (50, 610))
            okBtn.draw(win)
            okBtn.mark(win, 'T', (0, 255, 0))
            drawSidebar(win, game)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    RUN = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if okBtn.click(pos):
                        choosing = True
                        n.send("notchoosed")
        elif not started:
            btns = makeBoard(win, player, game.results(player))
            started = True
            if reset and player == 0:
                n.send("resetContinue")
                reset = False
        elif not finished:
            aPlayer = game.activePlayer()
            drawSidebar(win, game, aPlayer)
            if not moved and aPlayer == player:
                coor = game.getCoor()
                if coor != []:
                    btns[3*coor[0] + coor[1]].mark(win, game.marks[(player - 1)%2], game.colors[(player - 1)%2])
                moved = True
            if moved and game.activePlayer() != player:
                moved = False
            pygame.draw.rect(win, BGCOLOR, (50, 50, 500, 50))
            if aPlayer == player:
                text = FONT.render("Twój ruch!", 1, COMCOLOR)
            else:
                text = FONT.render("Czekasz na ruch gracza " + str(aPlayer), 1, COMCOLOR)
            win.blit(text, (50, 50))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    RUN = False
                    pygame.quit()
                    break
                if event.type == pygame.MOUSEBUTTONDOWN and player == aPlayer:
                   pos = pygame.mouse.get_pos()
                   for btn in btns:
                       if btn.click(pos) and game.place(btn.coor):
                           n.send(btn.print())
                           btn.mark(win, game.marks[player], game.colors[player])
            winner = game.win()
            if winner[0] != -1:
                if winner[0] == -2:
                    text = FONT.render("Brak ruchów - remis", 1, ACOLOR)
                    if player == 0:
                        n.send("tie")
                else:
                    if winner[0] == player:
                        text = FONT.render("Wygrałeś!", 1, ACOLOR)
                        n.send("win")
                    else:
                        text = FONT.render("Przegrałeś! Wygrał gracz " + str(winner[0]), 1, ACOLOR)
                    coor = winner[1][0]
                    dirc = winner[1][1]
                    startBtn = btns[3*coor[0] + coor[1]]
                    endBtn = btns[3*(coor[0] + 2*dirc[0]) + coor[1] + 2*dirc[1]]
                    cent = startBtn.size//2
                    pygame.draw.line(win, (255, 0, 0), (startBtn.x + cent, startBtn.y + cent), (endBtn.x + cent, endBtn.y + cent), 10)
                pygame.draw.rect(win, BGCOLOR, (50, 50, 500, 50))
                win.blit(text, (50, 50))
                text = FONT.render("Czy chcesz kontynuować?", 1, ACOLOR)
                yesBtn.draw(win)
                yesBtn.mark(win, "T", (0, 255, 0))
                noBtn.draw(win)
                noBtn.mark(win, "N", (255, 0, 0))
                win.blit(text, (50, 700))
                pygame.display.update()
                finished = True
        elif not game.continues[player]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    RUN = False
                    pygame.quit()
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if yesBtn.click(pos):
                        n.send("continue")
                        if player == 0:
                            n.send("reset")
                    if noBtn.click(pos):
                        run = False
                        RUN = False
        elif not game.continued():
            win.fill(BGCOLOR)
            font = pygame.font.SysFont("comicsans", 80)
            text = font.render("Czekasz na gracza " + str((player + 1)%2), 1, (255,0,0))
            win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    RUN = False
                    pygame.quit()
                    break
        else:
            started = False
            moved = False
            finished = False
            if player == 0:
                reset = True


def menu_screen():
    global RUN
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill(BGCOLOR)
        text = FONT.render("Kliknij by zagrać!", 1, (255,0,0))
        win.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                RUN = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    if RUN:
        main()

while RUN:
    menu_screen()
