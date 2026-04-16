from random import randint

class boardSpot(object):
    def __init__(self) -> None:
        self.value = 0          # 0-8 = safe, -1 = mine
        self.selected = False
        self.mine = False
        self.flagged = False
    
    def __str__(self) -> str:
        return str(self.value)
    
    def isMine(self):
        return self.value == -1
    
class classBoard(object):
    def __init__(self, i_boardSize, i_numMines, mines = None) -> None:
        self.board = [[boardSpot() for _ in range(i_boardSize)] for _ in range(i_boardSize)]
        self.boardSize = i_boardSize
        self.numMines = i_numMines
        self.selectableSpots = i_boardSize * i_boardSize - i_numMines
        
        if mines:
            for x, y in mines:
                self.addMine(x, y)
        else:
            # randomly place mines (no dupes)
            placed = 0
            while placed < i_numMines:
                x = randint(0, self.boardSize-1)
                y = randint(0, self.boardSize-1)
                if not self.board[x][y].mine:
                    self.addMine(x, y)
                    placed += 1
                
    def __str__(self) -> str:
        colW = max(3, len(str(self.boardSize - 1)) + 2)
        
        header = "   "
        for i in range(self.boardSize):
            header += str(i).center(colW)
        divider = "   " + "-" * (colW * self.boardSize)
        
        lines = [header, divider]
        
        for y in range(0, self.boardSize):
            rowStr = str(y).rjust(2) + " "
            for x in range(self.boardSize):
                spot = self.board[x][y]
                if spot.flagged and not spot.selected:
                    cell = "F"
                elif spot.selected and spot.mine:
                    cell = "M"
                elif spot.selected:
                    cell = str(spot.value)
                else:
                    cell = "-"
                rowStr += cell.center(colW)
            lines.append(rowStr)
        return "\n".join(lines)
                    
    def addMine(self, x, y):
        self.board[x][y].value = -1
        self.board[x][y].mine = True
        
        for nx in range(x - 1, x + 2):
            for ny in range(y - 1, y + 2):
                if nx == x and ny == y:
                    continue
                if 0 <= nx < self.boardSize and 0 <= ny < self.boardSize:
                    if not self.board[nx][ny].mine:
                        self.board[nx][ny].value += 1
                
    def makeMove(self, x, y):
        spot = self.board[x][y]
        
        if spot.selected or spot.flagged:
            return True
        
        spot.selected = True
        self.selectableSpots -= 1
        
        if spot.mine:
            return False
        
        if spot.value == 0:
            for nx in range(x - 1, x + 2):
                for ny in range(y - 1, y + 2):
                    if nx == x and ny == y:
                        continue
                    if 0 <= nx < self.boardSize and 0 <= ny < self.boardSize:
                        if not self.board[nx][ny].selected:
                            self.makeMove(nx, ny)
                            
        return True
    
    def revealAll(self):
        for x in range(self.boardSize):
            for y in range(self.boardSize):
                self.board[x][y].selected = True
        
    def toggleFlag(self, x, y):
        spot = self.board[x][y]
        if not spot.selected:
            spot.flagged = not spot.flagged
            return True
        print("Can't flag a revealed cell.")
        return False
        
    def hitMine(self, x, y):
        return self.board[x][y].mine
    
    def isWinner(self):
        return self.selectableSpots == 0
    
def getCoords(boardSize):
    while True:
        raw = input("Enter action and coordinates (e.g., 's 2 3' or 'f 1 4'): ").strip().split()
        if len(raw) != 3:
            print("  Please enter an action and 2 numbers (e.g., 's 2 3').")
            continue
        action = raw[0].lower()
        if action not in ('s', 'f'):
            print("  Invalid action. Use 's' to select or 'f' to flag.")
            continue
        try:
            x, y = int(raw[1]), int(raw[2])
        except ValueError:
            print(" Coordinates must be integers.")
            continue
        if not (0 <= x < boardSize and 0 <= y < boardSize):
            print(f"  Coordinates must be between 0 and {boardSize -1}.")
            continue
        return action, x, y
    
def play(mines=None):
    print("----- MINESWEEPER -----")
    
    while True:
        try:
            boardSize = int(input("Board size (width): "))
            print(boardSize)
            if boardSize < 2:
                print("  Board must be at least 2x2.")
                continue
            break
        except ValueError:
            print("  Please enter a whole number.")
            
    maxMines = boardSize * boardSize - 1
    while True:
        try:
            numMines = int(input(f"Number of mines (1-{maxMines}): "))
            print(numMines)
            if not (1 <= numMines <= maxMines):
                print(f"  Must be between 1 and {maxMines}.")
                continue
            break
        except ValueError:
            print("  Please enter a whole number.")
            
    board = classBoard(boardSize, numMines, mines)
    gameOver = False
    winner = False
    
    print("\n(s = select, f = (un)flag | e.g. 's 2 3')\n")
    
    while not gameOver:
        print("\nCurrent Board:")
        print(board)
        print()
        
        action, x, y = getCoords(boardSize)
        print(f"{action} {x} {y}")
        
        if action == 'f':
            board.toggleFlag(x, y)
        elif action == 's':
            spot = board.board[x][y]
            if spot.selected:
                print("  Cell already revealed.")
                continue
            elif spot.flagged:
                print("  Unflag the cell first ('f') before selecting.")
                continue
            
            safe = board.makeMove(x, y)
            
            if not safe:
                board.revealAll()
                print("\nCurrent Board:")
                print(board)
                print("\nBOOM! Game over.")
                gameOver = True
                
        if not gameOver and board.isWinner():
            print("\nCurrent Board:")
            print(board)
            print("\nCongrats you win!")
            gameOver = True
            
if __name__ == "__main__":
    try:
        play()
    except KeyboardInterrupt:
        print("\nGame exited.")