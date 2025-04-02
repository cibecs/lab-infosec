import numpy as np
from task7 import encryption, decryption  # Import encryption & decryption functions
from task4 import read_pairs_from_file  # Import function to read known pairs
from task1 import p
import random

dim = 4
n_guesses = 50000

def generate_random_key(dim, p):
    return np.array([random.randint(0, p-1) for _ in range(dim)])

def generate_key_guesses(n_guesses):
    key_prime = [generate_random_key(dim, p) for _ in range(n_guesses)]
    key_second = [generate_random_key(dim, p) for _ in range(n_guesses)]
    return key_prime, key_second

def generate_plaintext_ciphertext_from_keys(u, x, keys_prime, keys_second):
    ciphertexts = {}
    plaintexts = {}
    for kp in keys_prime:
        ciphertexts[tuple(kp)] = encryption(u, kp)
    for ks in keys_second:
        plaintexts[tuple(ks)] = decryption(x, ks)
    return ciphertexts, plaintexts

def look_for_matches(generated_ciphertexts, generated_plaintexts):
    matching_pairs = []
    for ks in generated_ciphertexts.keys():
        for kp in generated_plaintexts.keys():
            if np.array_equal(generated_ciphertexts[ks], generated_plaintexts[kp]):
                matching_pairs.append([{ks: generated_ciphertexts[ks]}, {kp: generated_plaintexts[kp]}])
    return matching_pairs

def main():
    # Define the filepath to the file containing plaintext-ciphertext pairs
    filepath = "KPAdataH_CyberDucks/KPAdataH/KPApairsH_linear.txt"
    
    # Read the plaintext-ciphertext pairs from the file
    original_plaintexts, original_ciphertexts = read_pairs_from_file(filepath)

    # Generate random key guesses
    keys_prime, keys_second = generate_key_guesses(n_guesses)

    # Generate encryption & decryption mappings
    generated_ciphertexts, generated_plaintexts = generate_plaintext_ciphertext_from_keys(
        original_plaintexts[0],
        original_ciphertexts[0],
        keys_prime,
        keys_second
    )
    
    # Look for key matches
    results = look_for_matches(generated_ciphertexts, generated_plaintexts)
    
    print(f"Found {len(results)} matching key pairs:")
    for match in results:
        print(match)

if __name__ == "__main__":
    main()
