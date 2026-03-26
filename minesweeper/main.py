from random import randint

class boardSpot(object):
    value = 0
    selected = False
    mine = False
    flagged = False
    
    def __init__(self) -> None:
        self.selected = False
        self.flagged = False
        
    def __str__(self) -> str:
        return str(boardSpot.value)
    
    def isMine(self):
        if boardSpot.value == -1:
            return True
        return False
    
class classBoard(object):
    def __init__(self, i_boardSize, i_numMines) -> None:
        self.board = [[boardSpot() for i in range(i_boardSize)] for j in range(i_boardSize)]
        self.boardSize = i_boardSize
        self.numMines = i_numMines
        self.selectableSpots = i_boardSize * i_boardSize - i_numMines
        
        i = 0
        while i < i_numMines:
            x = randint(0, self.boardSize-1)
            y = randint(0, self.boardSize-1)
            if not self.board[x][y].mine:
                self.addMine(x, y)
                i += 1
            else:
                i -= 1
                
    def __str__(self) -> str:
        returnString = " "
        divider = "\n---"
        
        for i in range(0, self.boardSize):
            returnString += " | " + str(i)
            divider += "----"
        divider += "\n"
        returnString += divider
        
        for y in range(0, self.boardSize):
            returnString += str(y)
            for x in range(0, self.boardSize):
                if self.board[x][y].flagged:
                    returnString += " | F"
                if self.board[x][y].mine and self.board[x][y].selected:
                    returnString += " |" + str(self.board[x][y].value)
                elif self.board[x][y].selected:
                    returnString += " | " + str(self.board[x][y])
                else:
                    returnString += " | "
            returnString += " |"
            returnString += divider
        return returnString
                    
    def addMine(self, x, y):
        self.board[x][y].value = -1
        self.board[x][y].mine = True
        for i in range(x - 1, x + 2):
            if i >= 0 and i < self.boardSize:
                if y - 1 >= 0 and not self.board[i][y - 1].mine:
                    self.board[i][y - 1].value += 1
                if y + 1 < self.boardSize and not self.board[i][y + 1].mine:
                    self.board[i][y + 1].value += 1
            if x - 1 >= 0 and not self.board[x - 1][y].mine:
                self.board[x - 1][y].value += 1
            if x + 1 < self.boardSize and not self.board[x + 1][y].mine:
                self.board[x + 1][y].value += 1
                
    def makeMove(self, x, y):
        self.board[x][y].selected = True
        self.selectableSpots -= 1
        if self.board[x][y].value == -1:
            return False
        if self.board[x][y].value == 0:
            for i in range(x - 1, x + 2):
                if i >= 0 and i < self.boardSize:
                    if y - 1 >= 0 and not self.board[i][y - 1].selected:
                        self.makeMove(i, y - 1)
                    if y + 1 < self.boardSize and not self.board[i][y + 1].selected:
                        self.makeMove(i, y + 1)
            if x - 1 >= 0 and not self.board[x + 1][y].selected:
                self.makeMove(x - 1, y)
            if x + 1 < self.boardSize and not self.board[x + 1][y].selected:
                self.makeMove(x + 1, y)
            return True
        else:
            return True
        
    def toggleFlag(self, x, y):
        if not self.board[x][y].selected:
            self.board[x][y].flagged = not self.board[x][y].flagged
            return True
        return False
        
    def hitMine(self, x, y):
        return self.board[x][y].value == -1
    
    def isWinner(self):
        return self.selectableSpots == 0
    
def play():
    boardSize = int(input("Choose the width of the board: "))
    numMines = int(input("Choose the number of mines: "))
        
    gameOver = False
    winner = False
    
    board = classBoard(boardSize, numMines)
    
    while not gameOver:
        print(board)
        print("(s for select, f for flag)\n(e.g., 's 1 2')\n")
        userInput = input("Enter action and coordinates: ").split()
        
        if len(userInput) != 3:
            print("Invalid input format.")
            continue
        
        action, strX, strY = userInput
        try:
            x, y = int(strX), int(strY)
        except ValueError:
            print("Invalid coordinates.")
            continue
        
        if action == 's':
            pass
        elif action == 'f':
            board.toggleFlag(x, y)
        else:
            print("Invalid action. Use 's' or 'f'.")
        
        if board.isWinner() and gameOver == False:
            gameOver = True
            winner = True
            
        print(board)
        if winner:
            print("Congrats, you won!")
        else:
            print("Game over, you hit a mine!")
            
play()