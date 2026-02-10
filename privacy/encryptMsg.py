def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            result += chr((ord(char) - offset + shift) % 26 + offset)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def brute_force_caesar(text):
    for key in range(1, 26):
        print(f"Key {key}: {caesar_decrypt(text, key)}")

# Example usage:
print("1. Encrypt")
print("2. Decrypt")
print("3. Brute Force")
choice = input("Enter your choice: ")

if choice == "1":
    message = input("Enter message to encrypt: ")
    key = int(input("Enter shift key (1-25): "))
    print("Encrypted:", caesar_encrypt(message, key))
elif choice == "2":
    message = input("Enter message to decrypt: ")
    key = int(input("Enter shift key (1-25): "))
    print("Decrypted:", caesar_decrypt(message, key))
elif choice == "3":
    message = input("Enter message to brute-force: ")
    brute_force_caesar(message)