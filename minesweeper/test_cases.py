import sys
from io import StringIO
from main import play

# Test case 1: Win the game
def test_win():
    inputs = [
        "3",  # board size
        "1",  # num mines
        "s 0 1",  # select safe spots
        "s 0 2",
        "s 1 0",
        "s 1 1",
        "s 1 2",
        "s 2 0",
        "s 2 1",
        "s 2 2"
    ]
    input_str = "\n".join(inputs) + "\n"
    sys.stdin = StringIO(input_str)
    print("Test Case 1: Winning the game")
    play(mines=[(0,0)])
    print("\n" + "="*50 + "\n")

# Test case 2: Lose the game
def test_lose():
    inputs = [
        "3",  # board size
        "1",  # num mines
        "s 0 0",  # select mine
    ]
    input_str = "\n".join(inputs) + "\n"
    sys.stdin = StringIO(input_str)
    print("Test Case 2: Losing the game")
    play(mines=[(0,0)])
    print("\n" + "="*50 + "\n")

# Test case 3: Flagging
def test_flag():
    inputs = [
        "3",  # board size
        "2",  # num mines
        "f 0 0",  # flag mines
        "f 1 1",
        "s 0 1",  # select safe
        "s 0 2",
        "s 1 0",
        "s 1 2",
        "s 2 0",
        "s 2 1",
        "s 2 2"
    ]
    input_str = "\n".join(inputs) + "\n"
    sys.stdin = StringIO(input_str)
    print("Test Case 3: Flagging mines")
    play(mines=[(0,0),(1,1)])
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    test_win()
    test_lose()
    test_flag()