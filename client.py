import pygame
from network import Network
import pickle
from constants import *
from button import Button as LongButton
from square_button import SquareButton as Button
from slider import Slider

pygame.font.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")
RUN = True
FONT = pygame.font.SysFont(FONT_NAME, FONT_SIZE)


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
    prevPlayer = 0
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
            if not moved and aPlayer != prevPlayer:
                coor = game.getCoor()
                if coor != []:
                    btns[3*coor[0] + coor[1]].mark(win, game.marks[prevPlayer], game.colors[prevPlayer])
                moved = True
            if moved and aPlayer == prevPlayer:
                moved = False
            prevPlayer = aPlayer
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
            text = font.render("Czekasz na resztę graczy", 1, (255,0,0))
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
    nButton = LongButton(WIDTH//2 - 50, HEIGHT//2 - 25, 200, 50)
    sButton = LongButton(WIDTH//2 - 50, HEIGHT//2 + 75, 200, 50)
    

    while run:
        clock.tick(60)
        win.fill(BGCOLOR)
        text = FONT.render("Kliknij by zagrać!", 1, (255,0,0))
        win.blit(text, (100,200))
        #nButton.draw(win)
        #sButton.draw(win)
        #nButton.write(win, "Stwórz nową grę", COMCOLOR)
        #sButton.write(win, "Znajdź grę", COMCOLOR)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                RUN = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                pos = pygame.mouse.get_pos()
                #if nButton.click(pos):
                 #   print("New")
                #if sButton.click(pos):
                  #  print("search")
    if RUN:
        main()

while RUN:
    menu_screen()
