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


def make_board(win, p, results, n=3):
    win.fill(BGCOLOR)
    text = FONT.render("Jesteś graczem " + str(p), 1, COM_COLOR)
    win.blit(text, (XMARGIN, 0))
    btns = [Button(i, j, n) for i in range (n) for j in range(n)]

    for btn in btns:
        btn.draw(win)
    text = FONT.render("Wygrane: " + results[0] + " Przegrane: " + results[1] + " Remis: " + results[2], 1, COM_COLOR)
    win.blit(text, (XMARGIN, HEIGHT - FONT_SIZE))
    return btns

def draw_select_mark(win, color):
    btns = [Button(i, j, 6) for i in range(6) for j in range(2)]
    for i in range(len(MARKS)):
        btns[i].draw(win)
        btns[i].mark(win, MARKS[i], color)
    return btns

def draw_sidebar(win, game, player=-1):
    btns = [[Button(13 + i, j, 12) for i in range(2)] for j in range(game.players)]
    for i in range(game.players):
        btns[i][0].draw(win)
        btns[i][1].draw(win)
        btns[i][0].mark(win, str(i), game.colors[i])
        btns[i][1].mark(win, game.marks[i], game.colors[i])
        if player == -1 and  game.choose[i]:
                btns[i][1].border(win, COM_COLOR)
    if player != -1:
        btns[player][1].border(win, ALERT_COLOR)
        
    
def main():
    run = True
    global RUN
    clock = pygame.time.Clock()
    n = Network()
    try:
        player = int(n.get_p())
    except:
        return
    print("You are player", player)
    previous_player = 0
    started = False
    choosing = True
    moved = False
    finished = False
    reset = False
    btns = []
    yes_btn = Button(10, 12, 12)
    no_btn = Button(11, 12, 12)
    ok_btn = LongButton(BOARD_SIZE, BOARD_SIZE, 2*FONT_SIZE, FONT_SIZE)
    current_choice = player
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
            font = pygame.font.SysFont(FONT_NAME, BIG_FONT_SIZE)
            text = font.render("Czekasz na gracza...", 1, RED, True)
            win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    RUN = False
                    pygame.quit()
        elif choosing:
            win.fill(BGCOLOR)
            text = FONT.render("Jesteś graczem " + str(player), 1, COM_COLOR)
            win.blit(text, (XMARGIN, FIRST_BAR))
            text = FONT.render("Wybierz symbol", 1, COM_COLOR)
            win.blit(text, (XMARGIN, SECOND_BAR))
            player_color = game.colors[player]
            select_btns = draw_select_mark(win, player_color)
            rgb_colors = [RED, GREEN, BLUE]
            sliders = [Slider(i, player_color[i], 'RGB'[i], rgb_colors[i]) for i in range(3)]
            for slider in sliders:
                slider.draw(win)
            text = FONT.render("Czy potwierdzasz wybór?", 1, COM_COLOR)
            win.blit(text, (XMARGIN, ACCEPT_BAR))
            ok_btn.draw(win)
            ok_btn.write(win, 'OK', GREEN)
            select_btns[current_choice].border(win, ALERT_COLOR)
            draw_sidebar(win, game)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    RUN = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btn in select_btns:
                        if btn.click(pos):
                            n.send('M' + btn.sign)
                            old_choice = current_choice
                            current_choice = 2*btn.coor[0] + btn.coor[1]
                    for slider in sliders:
                        if slider.click(pos):
                            n.send('C' + sliders[0].print() + sliders[1].print() + sliders[2].print())
                    if ok_btn.click(pos):
                        choosing = False
                        n.send("choosed")
        elif not game.choosed():
            win.fill(BGCOLOR)
            text = FONT.render("Jesteś graczem " + str(player), 1, COM_COLOR)
            win.blit(text, (XMARGIN, FIRST_BAR))
            text = FONT.render("Czekasz na innych graczy", 1, COM_COLOR, BGCOLOR)
            win.blit(text, (XMARGIN, ACCEPT_BAR//2))
            text = FONT.render("Chcesz wrócić do wybierania?", 1, COM_COLOR)
            win.blit(text, (XMARGIN, ACCEPT_BAR))
            ok_btn.draw(win)
            ok_btn.write(win, 'OK', GREEN)
            draw_sidebar(win, game)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    RUN = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if ok_btn.click(pos):
                        choosing = True
                        n.send("notchoosed")
        elif not started:
            btns = make_board(win, player, game.results(player))
            started = True
            if reset and player == 0:
                n.send("resetContinue")
                reset = False
        elif not finished:
            active_player = game.active_player()
            draw_sidebar(win, game, active_player)
            if not moved and active_player != previous_player:
                coor = game.get_coor()
                if coor != []:
                    btns[3*coor[0] + coor[1]].mark(win, game.marks[previous_player], game.colors[previous_player])
                moved = True
            if moved and active_player == previous_player:
                moved = False
            previous_player = active_player
            pygame.draw.rect(win, BGCOLOR, (XMARGIN, SECOND_BAR, BOARD_SIZE, FONT_SIZE))
            if active_player == player:
                text = FONT.render("Twój ruch!", 1, COM_COLOR)
            else:
                text = FONT.render("Czekasz na ruch gracza " + str(active_player), 1, COM_COLOR)
            win.blit(text, (XMARGIN, SECOND_BAR))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    RUN = False
                    pygame.quit()
                    break
                if event.type == pygame.MOUSEBUTTONDOWN and player == active_player:
                   pos = pygame.mouse.get_pos()
                   for btn in btns:
                       if btn.click(pos) and game.place(btn.coor):
                           n.send(btn.print())
                           btn.mark(win, game.marks[player], game.colors[player])
            winner = game.win()
            if winner[0] != -1:
                if winner[0] == -2:
                    text = FONT.render("Brak ruchów - remis", 1, ALERT_COLOR)
                    if player == 0:
                        n.send("tie")
                else:
                    if winner[0] == player:
                        text = FONT.render("Wygrałeś!", 1, ALERT_COLOR)
                        n.send("win")
                    else:
                        text = FONT.render("Przegrałeś! Wygrał gracz " + str(winner[0]), 1, ALERT_COLOR)
                    coor = winner[1][0]
                    dirc = winner[1][1]
                    start_btn = btns[3*coor[0] + coor[1]]
                    end_btn = btns[3*(coor[0] + 2*dirc[0]) + coor[1] + 2*dirc[1]]
                    cent = start_btn.size//2
                    pygame.draw.line(win, RED, (start_btn.x + cent, start_btn.y + cent), (end_btn.x + cent, end_btn.y + cent), 10)
                pygame.draw.rect(win, BGCOLOR, (XMARGIN, SECOND_BAR, BOARD_SIZE, FONT_SIZE))
                win.blit(text, (XMARGIN, SECOND_BAR))
                text = FONT.render("Czy chcesz kontynuować?", 1, ALERT_COLOR)
                yes_btn.draw(win)
                yes_btn.mark(win, "T", GREEN)
                no_btn.draw(win)
                no_btn.mark(win, "N", RED)
                win.blit(text, (XMARGIN, SECRET_BAR))
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
                    if yes_btn.click(pos):
                        n.send("continue")
                        if player == 0:
                            n.send("reset")
                    if no_btn.click(pos):
                        run = False
                        RUN = False
        elif not game.continued():
            win.fill(BGCOLOR)
            font = pygame.font.SysFont(FONT_NAME, BIG_FONT_SIZE)
            text = font.render("Czekasz na resztę graczy", 1, RED)
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
    new_button = LongButton(WIDTH//2 - 50, HEIGHT//2 - 25, 5*FONT_SIZE, FONT_SIZE)
    join_button = LongButton(WIDTH//2 - 50, HEIGHT//2 + 75, 5*FONT_SIZE, FONT_SIZE)
    

    while run:
        clock.tick(60)
        win.fill(BGCOLOR)
        text = FONT.render("Kliknij by zagrać!", 1, RED)
        win.blit(text, (XMARGIN, SECOND_BAR))
        #new_button.draw(win)
        #join_button.draw(win)
        #new_button.write(win, "Stwórz nową grę", COM_COLOR)
        #join_button.write(win, "Znajdź grę", COM_COLOR)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                RUN = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                pos = pygame.mouse.get_pos()
                #if new_button.click(pos):
                 #   print("new")
                #if join_button.click(pos):
                  #  print("join")
    if RUN:
        main()

while RUN:
    menu_screen()
