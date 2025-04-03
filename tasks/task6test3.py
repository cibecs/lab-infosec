from task1 import p
from task5 import encryption
from task2 import modular_inverse_matrix
from task4 import read_pairs_from_file
import numpy as np              

C = np.identity(8, dtype=int) # Identity matrix of size 8x8 

# Function to generate matrices A and B
def generate_matrix_A_B():
    dim = 8  # Dimension of the matrices
    # Initialize matrices A and B with zeros
    A_matrix = np.zeros((dim, dim), dtype=int)
    B_matrix = np.zeros((dim, dim), dtype=int)

    # Compute matrix A: E(e_j, 0)
    for j in range(dim):
        # Create the unit vector e_j
        e_j = np.zeros(dim, dtype=int)
        e_j[j] = 1
        # Use e_j as the key and a zero vector as the input
        k = e_j
        u = np.zeros(dim, dtype=int)
        # Encrypt and store the result in the j-th column of A
        A_matrix[:, j] = encryption(u, k)

    # Compute matrix B: E(0, e_j)
    for j in range(dim):
        # Create the unit vector e_j
        e_j = np.zeros(dim, dtype=int)
        e_j[j] = 1
        # Use a zero vector as the key and e_j as the input
        k = np.zeros(dim, dtype=int)
        u = e_j
        # Encrypt and store the result in the j-th column of B
        B_matrix[:, j] = encryption(u, k)

    # Return the computed matrices A and B
    return A_matrix, B_matrix


def recover_one_key(u, x, A, B):
    # Compute the modular inverse of matrix A 
    A_inv = modular_inverse_matrix(A)
    # Compute the product of matrix B and vector u 
    Bu = (B @ u) 
    # Compute the product of matrix C and vector x
    Cx = (C @ x) 
    # Compute the difference between the Cx and Bu 
    diff = (Cx - Bu) 
    # Compute the key k using the formula: k = A_inv @ diff % p
    k = (A_inv @ diff) % p
    return k


def find_keys(plaintexts, ciphertexts):
    A, B = generate_matrix_A_B()
    # Iterate over all plaintext-ciphertext pairs
    for i in range(len(plaintexts)):
        u = plaintexts[i]
        x = ciphertexts[i]
        k = recover_one_key(u, x, A, B)
        print("Key found:", k)

        total_hamming = 0
        for j in range(len(plaintexts)):
            u_current = plaintexts[j]
            x_current = ciphertexts[j]
            x_test = encryption(u_current, k)

            hamming = np.sum(x_current != x_test)
            total_hamming += hamming

        print("Total Hamming Distance:", total_hamming)

def improve_key(key, plaintexts, ciphertexts, max_steps=1000):
    current_key = key.copy()
    current_hamming = total_hamming_distance(current_key, plaintexts, ciphertexts)
    steps = 0

    while steps < max_steps:
        improved = False
        for i in range(len(current_key)):
            original_value = current_key[i]
            for val in range(p):
                if val == original_value:
                    continue
                new_key = current_key.copy()
                new_key[i] = val
                new_hamming = total_hamming_distance(new_key, plaintexts, ciphertexts)
                if new_hamming < current_hamming:
                    print(f"Improved: {current_key} → {new_key} | Hamming: {current_hamming} → {new_hamming}")
                    current_key = new_key
                    current_hamming = new_hamming
                    improved = True
                    break
            if improved:
                break
        if not improved:
            break
        steps += 1

    print("Final key:", current_key)
    print("Final Hamming Distance:", current_hamming)
    return current_key


def total_hamming_distance(key, plaintexts, ciphertexts):
    total = 0
    for u, x in zip(plaintexts, ciphertexts):
        x_test = encryption(u, key)
        total += np.sum(x != x_test)
    return total



        
# Define the filepath to the file containing plaintext-ciphertext pairs
filepath = "KPAdataH_CyberDucks/KPAdataH/KPApairsH_nearly_linear.txt"
# Read the plaintext-ciphertext pairs from the file
plaintexts, ciphertexts = read_pairs_from_file(filepath)
find_keys(plaintexts, ciphertexts)
key1 = [10,1,6,3,0,8,2,10]
improve_key(key1, plaintexts, ciphertexts)
