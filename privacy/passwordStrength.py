import time
import random
import string

# Simulated dictionary of 10,000 words (for example purposes)
word_list = [f"word{i}" for i in range(1000)]

def brute_force_simulation(password, candidates):
    attempts = 0
    start_time = time.time()
    for guess in candidates:
        attempts += 1
        if guess == password:
            break
    end_time = time.time()
    return end_time - start_time, attempts

def generate_password(word_count=1, add_digit=False):
    words = random.sample(word_list, word_count)
    if add_digit:
        digit = str(random.randint(0, 9))
        return ''.join(words) + digit
    return ''.join(words)

def create_candidates(word_count, add_digit):
    from itertools import product

    if word_count == 1:
        return [w for w in word_list]
    elif word_count == 2 and not add_digit:
        return [w1 + w2 for w1 in word_list for w2 in word_list]
    elif word_count == 2 and add_digit:
        return [w1 + w2 + str(d) for w1 in word_list for w2 in word_list for d in range(10)]

def average_time(word_count, add_digit=False, trials=1):
    total_time = 0
    total_attempts = 0
    candidates = create_candidates(word_count, add_digit)
    for _ in range(trials):
        password = generate_password(word_count, add_digit)
        random.shuffle(candidates)  # simulate guessing randomness
        time_taken, attempts = brute_force_simulation(password, candidates)
        total_time += time_taken
        total_attempts += attempts
    avg_time = total_time / trials
    avg_attempts = total_attempts / trials
    return avg_time, avg_attempts

# Run simulations
print("Running brute-force simulation...")

for wc, desc, digit in [
    (1, "One-word", False),
    (2, "Two-word", False),
    (2, "Two-word with digit", True)
]:
    t, a = average_time(wc, digit, trials=1)
    print(f"{desc} password:")
    print(f"  Average Time: {t:.4f} seconds")
    print(f"  Average Attempts: {int(a)}\n")