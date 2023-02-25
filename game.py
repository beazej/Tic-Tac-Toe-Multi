class Game:
    def __init__(self, id):
        self.ready = False
        self.id = id
        self.wins = [0,0]
        self.ties = 0
        self.moving = [True, False]
        self.board = [[-1 for i in range(3)] for j in range(3)]
        self.lastCoor = [] 
        self.size = 3
        self.colors = [(255, 0, 0), (0, 255, 0)]
        self.marks = ['X', 'O'] 
        self.continues = [False, False]

    def activePlayer(self):
        for i in range(len(self.moving)):
            if self.moving[i]:
                return i

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

    def row(self, k, i, j, dirc):
        if self.board[i][j] == -1:
            return False
        for ki in range(1, k):
            if 0 <= i + dirc[0]*ki < self.size and 0 <= j + dirc[1]*ki < self.size:
                if self.board[i + dirc[0]*ki][j + dirc[1]*ki] != self.board[i][j]:
                    return False
            else:
                return False
        return True

    def win(self):
        for i in range(self.size):
            for j in range(self.size):
                for dirc in [[1, 0], [0, 1], [1, 1], [1, -1]]:
                    if self.row(3, i, j, dirc):
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
