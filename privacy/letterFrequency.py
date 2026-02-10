def letter_frequency(text):
    text = text.lower()  # normalize to lowercase
    frequency = {}

    for char in text:
        if char.isalpha():  # count only letters
            if char in frequency:
                frequency[char] += 1
            else:
                frequency[char] = 1

    total_letters = sum(frequency.values())

    print(" Letter Frequencies:\n")
    for letter in sorted(frequency):
        percent = (frequency[letter] / total_letters) * 100
        print(f"{letter.upper()} : {frequency[letter]} times ({percent:.2f}%)")

# Example usage
input_text = input("Enter a message to analyze: ")
letter_frequency(input_text)