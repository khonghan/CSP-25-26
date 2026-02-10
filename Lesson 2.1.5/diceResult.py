# Print the program title
print("Dice Game Result Checker")

try:
    # Get user input and convert to integer
    roll = int(input("Enter the result of your dice roll (1-6): "))
    # Check if the roll is within the valid range
    if roll < 1 or roll > 6:
        raise ValueError("Must be an integer between 1 and 6.")
except ValueError:
    # Handle the case where there's an invalid input
    print("Invalid input. Please try again and enter an integer between 1 and 6.")
    exit()

# Check dice roll value and print corresponding result
if roll == 1:
    print("Loser! You get nothing.") # Rolling 1 is a loss
elif roll == 6: # Rolling 6 is a jackpot win
    print("Winner! You get $1,000,000!")
elif roll == 2 or roll == 5:
    print("You win 2 cents.")
elif roll == 4 or roll == 3:
    print("You win a piece bread.")
else:
    print("Invalid! Please enter a number between 1 and 6.")

'''
1. The hardest bug to fix was making sure that the program only accepted integers between 1 and 6 and handled
invalid inputs/values that were outside this range, as the expected outcome didn't initially come the first time
when attempting to debug this code. It was hard to fix because the relational operators were originally hard to 
read with the several ands/ors.

2. Heavily testing helped with finding logical problems since it was stated what was wrong in the terminal after
I made small adjustments to the code. I tested with various inputs, like valid numbers, invalid strings, and edge
cases. By observing how the program responded to these different inputs, I was able to figure out where the logic
needed adjustment and ensure it could be handled correctly.

3. One thing that I'll do in the future to prevent sloppy code is to ensure clean and organized code formatting
with proper indentation and spacing as it will help me stay organized with the code--improving its readability.
'''

