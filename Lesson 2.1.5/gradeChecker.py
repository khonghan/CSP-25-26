# Print the program title
print("Grade Checker")

try:
    # Get user input and convert to integer
    grade = int(input("Enter your test score (0-100): "))
    # Check if the grade is within the valid range
    if grade < 0 or grade > 100:
        raise ValueError("Must be a positive integer between 0 and 100.")
except ValueError:
    # Handle the case where there's an invalid input
    print("Invalid input. Please try again and enter an integer between 0 and 100.")
    exit()

# Determine the letter grade based on the numeric grade
if grade >= 90: # Grade is between 90 and 100
    print("You received an A.")
elif grade >= 80: # Grade is between 80 and 89
    print("You received a B.")
elif grade >= 70: # Grade is between 70 and 79
    print("You received a C.")
elif grade >= 60: # Grade is between 60 and 69
    print("You received a D.")
else: # Grade is below 60
    print("You received an F.")

'''
1. The hardest bug to fix was making sure the input accepted only integers between 0 
through 100 and handling invalid inputs or values outside this range. This was hard 
to fix because it required careful input validation and error handling to ensure the 
program behaved correctly under any and all conditions/circumstances.

2. Testing helped me identify these issues by allowing me to see how the program behaved
with different inputs. I did this by testing edge cases (e.g., 0, 100, and invalid inputs)
and observing what the program outputted. This helped me figure out where the program was
not handling certain cases properly, allowing me to fix the logic accordingly.

3. One thing that I'll do in future projects to avoid writing sloppy code is to comment what
the program should do and what each section of code does. This will help me stay organized
and make it easier to debug and maintain the code in the future.
'''



