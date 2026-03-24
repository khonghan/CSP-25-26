import tkinter as tk
from tkinter import messagebox

class TicTacToeGame:
    def __init__(self):
        # 9 elements representing the board, index 0–8 ("" (empty), "X", or "O")
        self.board = [""] * 9
        self.currentPlayer = "X"
        self.gameOver = False

    def reset(self):
        # reset the game to original state
        self.board = [""] * 9
        self.currentPlayer = "X"
        self.gameOver = False

    def makeMove(self, index) -> bool:
        # try to place the current player's symbol at the given index; returns True if the move was made, False if invalid.
        if self.gameOver:
            return False
        if self.board[index] != "":
            # space already taken
            return False
        self.board[index] = self.currentPlayer
        return True

    def switchPlayer(self):
        # switch between X and O
        self.currentPlayer = "O" if self.currentPlayer == "X" else "X"

    def checkWinner(self):
        winningLines = [
            # rows
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            # columns
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            # diagonals
            (0, 4, 8),
            (2, 4, 6),
        ]

        for a, b_i, c in winningLines:
            if (
                self.board[a] != ""
                and self.board[a] == self.board[b_i] == self.board[c]
            ):
                return self.board[a], [a, b_i, c]

        return None, []

    def isDraw(self) -> bool:
        # return True if the board is full and there is no winner
        if "" in self.board:
            return False
        winner, _ = self.checkWinner()
        return winner is None


class TicTacToeGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.geometry("360x430")
        self.root.resizable(False, False)

        self.game = TicTacToeGame()

        # list of 9 button widgets corresponding to board indices 0–8
        self.buttons: list[tk.Button] = []

        self.createWidgets()

    def createWidgets(self):
        # title / status label
        self.statusLabel = tk.Label(
            self.root,
            text="Player X's turn",
            font=("Helvetica", 16, "bold"),
            pady=10,
        )
        self.statusLabel.pack()

        # frame for the 3x3 grid
        gridFrame = tk.Frame(self.root)
        gridFrame.pack(pady=10)

        # create 9 buttons in a loop
        for index in range(9):
            row = index // 3
            col = index % 3
            button = tk.Button(
                gridFrame,
                text="",
                font=("Helvetica", 36, "bold"),
                width=3,
                height=1,
                command=lambda i=index: self.handleButtonClick(i),
            )
            button.grid(row=row, column=col, padx=5, pady=5)
            self.buttons.append(button)

        # reset button
        resetButton = tk.Button(
            self.root,
            text="Reset Game",
            font=("Helvetica", 12),
            command=self.resetGame,
            width=15,
        )
        resetButton.pack(pady=15)

    def handleButtonClick(self, index):
        if self.game.gameOver:
            return

        # try to make the move in the game logic
        moveMade = self.game.makeMove(index)
        if not moveMade:
            # space taken – ignore
            return

        # update button text and disable further clicks on that button
        self.buttons[index].config(text=self.game.currentPlayer, state="disabled")

        # check for a winner
        winner, winningIndices = self.game.checkWinner()
        if winner:
            self.game.gameOver = True
            self.highlightWinningLine(winningIndices)
            self.statusLabel.config(text=f"Player {winner} wins!")
            messagebox.showinfo("Game Over", f"Player {winner} wins!")
            self.disableAllButtons()
            return

        # check for a draw
        if self.game.isDraw():
            self.game.gameOver = True
            self.statusLabel.config(text="It's a draw!")
            messagebox.showinfo("Game Over", "It's a draw!")
            self.disableAllButtons()
            return

        # no winner or draw – switch players and update status
        self.game.switchPlayer()
        self.statusLabel.config(text=f"Player {self.game.currentPlayer}'s turn")

    def highlightWinningLine(self, indices):
        for i in indices:
            self.buttons[i].config(bg="lightgreen")

    def disableAllButtons(self):
        for btn in self.buttons:
            btn.config(state="disabled")

    def resetGame(self):
        self.game.reset()
        for btn in self.buttons:
            btn.config(text="", state="normal", bg="SystemButtonFace")
        self.statusLabel.config(text="Player X's turn")


def main():
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()


"""
What was the hardest part?
- The hardest part was keeping the game state in sync between the list that tracks the board and 
the actual buttons on the screen, especially when checking all the different winning combinations 
and making sure the game stopped at the right time.

What did you learn?
- I learned how to connect Tkinter button events to functions, how to use a list to represent a 
3x3 board with indices, and how to separate game logic (a class that tracks the board and 
checks for wins/draws) from the GUI code that only handles display and user interaction.

What would you improve?
- In the future I would add a way to keep score across multiple rounds, maybe add a start menu 
or option to choose who goes first, and organize the code into separate files so the GUI and 
logic are even more clearly separated.
"""

