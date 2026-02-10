def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def modinv(e, phi):
    # Extended Euclidean Algorithm
    d_old, r_old = 0, phi
    d_new, r_new = 1, e
    while r_new != 0:
        quotient = r_old // r_new
        d_old, d_new = d_new, d_old - quotient * d_new
        r_old, r_new = r_new, r_old - quotient * r_new
    return d_old % phi

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def generate_keys():
    print("Choose two small prime numbers (e.g. 17 and 23):")
    p = int(input("Enter prime p: "))
    q = int(input("Enter prime q: "))
    if not (is_prime(p) and is_prime(q)):
        print("Both numbers must be prime.")
        return

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose e
    e = 3
    while gcd(e, phi) != 1:
        e += 2

    # Compute d
    d = modinv(e, phi)

    print(f"\n Public Key: ({e}, {n})")
    print(f" Private Key: {d}")
    return e, d, n

def encrypt(message, e, n):
    encrypted = [pow(ord(char), e, n) for char in message]
    return encrypted

def decrypt(cipher, d, n):
    decrypted = ''.join([chr(pow(char, d, n)) for char in cipher])
    return decrypted

# Example use
print(" RSA Cryptosystem")
choice = input("1. Generate keys\n2. Encrypt\n3. Decrypt\nChoose option: ")

if choice == "1":
    generate_keys()

elif choice == "2":
    msg = input("Enter your message: ")
    e = int(input("Enter recipient's public key e: "))
    n = int(input("Enter recipient's public key n: "))
    encrypted_msg = encrypt(msg, e, n)
    print(" Encrypted message:", encrypted_msg)

elif choice == "3":
    cipher_input = input("Paste the encrypted message as a list (e.g. [123, 456, ...]): ")
    cipher = eval(cipher_input)
    d = int(input("Enter your private key d: "))
    n = int(input("Enter your modulus n: "))
    decrypted_msg = decrypt(cipher, d, n)
    print(" Decrypted message:", decrypted_msg)
