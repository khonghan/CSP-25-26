import pprint
from random import randint

def initBoard(size, numMines):
    board = [[0 for _ in range(size)] for _ in range(size)]
    minesPlaced = 0
    
    # place mines
    while minesPlaced < numMines:
        r = randint(0, size - 1)
        c = randint(0, size - 1)
        if board[r][c] != -1:
            board[r][c] = -1
            minesPlaced += 1
            
    for r in range(size):
        for c in range(size):
            if board[r][c] == -1:
                continue
            # check neighbor cells
            for i in range(-1, 2):
                for j in range(-1, 2):
                    nr, nc = r + i, c + j
                    if 0 <= nr < size and 0 <= nc < size and board[nr][nc] == -1:
                        board[r][c] += 1
    return board

initBoard(10, 10)