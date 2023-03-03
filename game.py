from constants import *

class Game:
    def __init__(self, id, players=2):
        self.players = players
        self.ready = False
        self.id = id
        self.wins = [0 for i in range(self.players)]
        self.ties = 0
        self.size = 3
        self.rowSize = 3
        self.moving = [True] + [False for i in range(self.players - 1)]
        self.board = [[-1 for i in range(self.size)] for j in range(self.size)]
        self.lastCoor = [] 
        self.colors = [((i+1)%2*200, i%5*60, i//5*200) for i in range(self.players)]
        self.marks = [MARKS[i] for i in range(self.players)] 
        self.continues = [False for i in range(self.players)]
        self.choose = [False for i in range(self.players)]

    def setColor(self, player, color):
        self.colors[player] = (int(color[:3]), int(color[3:6]), int(color[6:]))

    def activePlayer(self):
        for i in range(len(self.moving)):
            if self.moving[i]:
                return i

    def choosed(self):
        return all(self.choose)

    def continued(self):
        return self.continues[0] and self.continues[1]

    def resetContinue(self):
        self.continues = [False, False]

    def play(self, player, move):
        i = int(move[:2])
        j = int(move[2:])
        self.board[i][j] = player
        self.moving[player] = False
        self.moving[(player + 1)%2] = True
        self.lastCoor = [i,j]

    def getCoor(self):
        return self.lastCoor

    def place(self, coor):
        if self.board[coor[0]][coor[1]] == -1:
            return True
        else:
            return False

    def connected(self):
        return self.ready

    def row(self, i, j, dirc):
        if self.board[i][j] == -1:
            return False
        for k in range(1, self.rowSize):
            if 0 <= i + dirc[0]*k < self.size and 0 <= j + dirc[1]*k < self.size:
                if self.board[i + dirc[0]*k][j + dirc[1]*k] != self.board[i][j]:
                    return False
            else:
                return False
        return True

    def win(self):
        for i in range(self.size):
            for j in range(self.size):
                for dirc in [[1, 0], [0, 1], [1, 1], [1, -1]]:
                    if self.row(i, j, dirc):
                        return [self.board[i][j], [[i, j], dirc]]
        if not any(-1 in b for b in self.board):
            return [-2, None]
        return [-1, None]

    def results(self, p):
        w = str(self.wins[p])
        p = str(sum(self.wins) - self.wins[p])
        t = str(self.ties)
        return [w, p, t]

    def reset(self):
        self.board = [[-1 for i in range(3)] for j in range(3)]
        self.moving = [True, False]
        self.lastCoor = [] 
