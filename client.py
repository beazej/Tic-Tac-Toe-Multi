import pygame
from network import Network
import pickle
pygame.font.init()

WIDTH = 700
HEIGHT = 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")
RUN = True
FONT = pygame.font.SysFont("comicsans", 50)
BGCOLOR = (192, 192, 192)
COMCOLOR = (0, 0, 255)
ACOLOR = (200, 50, 0)

class Button:
    def __init__(self, i, j, n):
        self.n = n
        self.color = BGCOLOR
        self.size = (WIDTH - 100)//self.n
        self.x = 50 + i*self.size
        self.y = 100 + j*self.size
        self.coor = [i, j]

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.size, self.size), 1)

    def mark(self, mark, color):
        font = pygame.font.SysFont("comicsans", self.size)
        text = font.render(mark, 1, color)
        win.blit(text, (self.x + self.size//4, self.y + self.size//4))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.size and self.y <= y1 <= self.y + self.size:
            return True
        else:
            return False

    def print(self):
        text = ''
        for i in range(2):
            if self.coor[i] < 10:
                text += '0' +  str(self.coor[i])
            else:
                text += str(self.coor[i])
        return text

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
    
def main():
    run = True
    global RUN
    clock = pygame.time.Clock()
    n = Network()
    started = False
    moved = False
    finished = False
    reset = False
    player = int(n.getP())
    print("You are player", player)
    btns = []
    yesBtn = Button(10, 12, 12)
    noBtn = Button(11, 12, 12)
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
            text = font.render("Czekamy na drugiego gracza...", 1, (255,0,0), True)
            win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    RUN = False
                    pygame.quit()
        elif not started:
            btns = makeBoard(win, player, game.results(player))
            started = True
            if reset and player == 0:
                n.send("resetContinue")
                reset = False
        elif not finished:
            aPlayer = game.activePlayer()
            if not moved and aPlayer == player:
                coor = game.getCoor()
                if coor != []:
                    btns[3*coor[0] + coor[1]].mark(game.marks[(player - 1)%2], game.colors[(player - 1)%2])
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
                       if btn.click(pos) and game.place(btn.coor)  and game.connected():
                           n.send(btn.print())
                           btn.mark(game.marks[player], game.colors[player])
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
                yesBtn.mark("T", (0, 255, 0))
                noBtn.draw(win)
                noBtn.mark("N", (255, 0, 0))
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
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Kliknij by zagrać!", 1, (255,0,0))
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
