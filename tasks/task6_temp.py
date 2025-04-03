from task1 import p
from task5 import encryption
from task2 import modular_inverse_matrix
from task4 import read_pairs_from_file

from task7 import modular_inverse

import numpy as np              

# Function to generate matrices A and B
def generate_matrix_A_B():
    dim = 8  # Dimension of the matrices
    # Initialize matrices A and B with zeros
    A_matrix = np.zeros((dim, dim), dtype=int)
    B_matrix = np.zeros((dim, dim), dtype=int)
    C_matrix = np.zeros((dim, dim), dtype=int)

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

        #trovo matrice C
        C_matrix[:, j] = (A_matrix[:, j] @ k.reshape(-1, 1)) * modular_inverse(encryption(u, k)) % p

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
    return A_matrix, B_matrix, C_matrix

def recover_one_key(u, x, A, B, C):
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
    A, B, C = generate_matrix_A_B()
    # Print the matrices A, B, and C
    print("Matrix A:\n", A)
    print("Matrix B:\n", B)
    print("Matrix C:\n", C)

    #NON E' DETTO CHE A E B SI TROVINO COSI'
    # Iterate over all plaintext-ciphertext pairs
    for i in range(len(plaintexts)):
        u = plaintexts[i]
        x = ciphertexts[i]
        k = recover_one_key(u, x, A, B, C)
        print("Key found:", k)
        count_true = 0
        count_false = 0

        for j in range(len(plaintexts)):
            u_current = plaintexts[j]
            x_current = ciphertexts[j]
            # Compute the encryption of the plaintext u using the key k
            x_test = encryption(u_current, k)
            print(x_test)
            # Check if the computed ciphertext matches the given ciphertext
            if not np.array_equal(x_current, x_test):
                count_false += 1
            else:
                count_true += 1
        print("Number of mismatches:", count_false)
        print("Number of matches:", count_true)

        
# Define the filepath to the file containing plaintext-ciphertext pairs
filepath = "KPAdataH_CyberDucks/KPAdataH/KPApairsH_nearly_linear.txt"
# Read the plaintext-ciphertext pairs from the file
plaintexts, ciphertexts = read_pairs_from_file(filepath)
find_keys(plaintexts, ciphertexts)