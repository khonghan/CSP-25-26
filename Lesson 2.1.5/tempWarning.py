# Print the program title
print("Temperature Warning System")

try:
    temp_input = input("Enter the temperature in Fahrenheit: ")
    # Reject numbers with leading zeros (except '0' or numbers like '0.5')
    if temp_input.startswith('0') and not (temp_input == '0' or temp_input.startswith('0.') or temp_input.startswith('-0.') or temp_input.startswith('+0.')):
        raise ValueError("Temperature cannot start with a leading zero.")
    temp = float(temp_input)
    # Check if the temperature is within valid range
    if temp < -128.6 or temp > 134:
        # -128.6°F is the lowest recorded temperature on Earth
        # 134°F is the highest recorded temperature on Earth
        raise ValueError("Temperature must be between -128.6°F and 134°F.")
except ValueError:
    # Handle the case where the input is not a valid number
    print("Invalid input. Please enter a numeric value for the temperature.")
    exit()


# Check the temperature and print the appropriate message
if temp <= 32:
    # Extreme cold warning if the temperature is 32°F or below
    print("Warning: It's extremely cold outside!")
elif temp >= 90:
    # Extreme heat warning if the temperature is 90°F or above
    print("Warning: It's extremely hot outside!")
else:
    # No warning if the temperature is between 33°F and 89°F
    print("The temperature is moderate.")

'''
1. The hardest bug to fix was ensuring that the program only accepted valid numeric inputs and handled the edge cases correctly (e.g., leading zeros,
non-numeric values, and out-of-range temperatures). This was challenging because it required careful input validation and error handling to make sure
that the program behaved correctly under all conditions. Overall, the hardest part was fixing the temperature range to accept realistic values only.

2. Testing helped me identify which parts of the code weren't functioning as expected or allowed invalid inputs. I tested the program with various
inputs, like valid temperatures, invalid strings, and edge cases (e.g., -128.6, 134, 0, 32, 90). By observing the program's output for these different
inputs, I was able to pinpoint where the logic needed adjustment and ensure that all scenarios were handled correctly.

3. One thing I'll do in the future to avoid writing sloppy code is to write clear comments explaining what each section of code does and background
information about the logic. It will help me stay organized and make it easier to maintain and debug the code later on.
'''