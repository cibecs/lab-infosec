from task1 import encryption, p
from task2 import modular_inverse_matrix
from task3 import generate_matrix_A_B
from task4 import read_pairs_from_file
import numpy as np              

x_test = [9, 0, 0, 0, 5, 0, 0, 6]
# Ak + Bu mod p = x -->modular_inverse_matrix 
# Ak + Bu + Cx == 0 mod p
# Cx = -Ak - Bu mod p
# Could be equal I
#

# Ak == -Bu -Cx mod p
# k = A^-1(-Bu -Cx) mod p
# check if k is equal to the original k

C = np.identity(8, dtype=int) # Identity matrix of size 8x8

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
        count_true = 0
        count_false = 0

        for j in range(len(plaintexts)):
            u_current = plaintexts[j]
            x_current = ciphertexts[j]
        # Compute the encryption of the plaintext u using the key k
            x_test = encryption(u_current, k)
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
