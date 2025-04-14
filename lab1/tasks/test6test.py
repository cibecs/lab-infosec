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

def compute_matrix_C_identity(dim):
    """
    Start with the identity matrix as the initial assumption for C.
    """
    return np.identity(dim, dtype=int)

def compute_matrix_C_dynamic(dim):
    """
    Compute the matrix C dynamically based on the cipher's behavior.
    """
    C_matrix = np.zeros((dim, dim), dtype=int)

    for j in range(dim):
        # Create the unit vector e_j
        e_j = np.zeros(dim, dtype=int)
        e_j[j] = 1
        # Encrypt e_j with itself as the key to observe the effect on the ciphertext
        k = e_j  # Use the unit vector as the key
        transformed = encryption(e_j, k)
        C_matrix[:, j] = transformed

    print("Matrix C (recomputed dynamically):\n", C_matrix)
    return C_matrix

# Function to recover one key using linear approximation
def recover_one_key(u, x, A, B, C):
    # Compute the modular inverse of matrix A 
    A_inv = modular_inverse_matrix(A)
    # Compute the product of matrix B and vector u 
    Bu = (B @ u) % p
    # Compute the product of matrix C and vector x
    Cx = (C @ x) % p
    # Compute the difference between the Cx and Bu 
    diff = (Cx - Bu) % p
    # Compute the key k using the formula: k = A_inv @ diff % p
    k = (A_inv @ diff) % p
    return k

# Function to find keys using linear cryptanalysis
def find_keys(plaintexts, ciphertexts):
    A, B = generate_matrix_A_B()
    dim = 8  # Dimension of the matrices

    # Start with C = I
    C = compute_matrix_C_identity(dim)

    # Print the matrices A, B, and initial C
    print("Matrix A:\n", A)
    print("Matrix B:\n", B)
    print("Initial Matrix C (Identity):\n", C)

    # Evaluate the probability of the linear approximation
    total_pairs = len(plaintexts)
    correct_count = 0

    for i in range(total_pairs):
        u = plaintexts[i]
        x = ciphertexts[i]
        k = np.random.randint(0, p, size=(dim,), dtype=int)  # Random key for testing
        approx = (A @ k + B @ u + C @ x) % p  # Use a non-zero key
        if np.all(approx == 0):
            correct_count += 1

    probability = correct_count / total_pairs
    print(f"Probability of linear approximation: {probability}")

    # Check if the probability is greater than 1 / p^lx
    threshold = 1 / (p ** dim)
    if probability > threshold:
        print(f"Linear approximation is valid (P > {threshold}).")
    else:
        print(f"Linear approximation is invalid (P <= {threshold}). Recomputing C...")

        # Recompute C dynamically
        C = compute_matrix_C_dynamic(dim)

        # Re-evaluate the probability with the new C
        correct_count = 0
        for i in range(total_pairs):
            u = plaintexts[i]
            x = ciphertexts[i]
            k = np.random.randint(0, p, size=(dim,), dtype=int)  # Random key for testing
            approx = (A @ k + B @ u + C @ x) % p  # Use a non-zero key
            if np.all(approx == 0):
                correct_count += 1

        probability = correct_count / total_pairs
        print(f"Probability of linear approximation after recomputing C: {probability}")
        if probability > threshold:
            print(f"Linear approximation is now valid (P > {threshold}).")
        else:
            print(f"Linear approximation is still invalid (P <= {threshold}).")

    # Perform key recovery
    for i in range(len(plaintexts)):
        u = plaintexts[i]
        x = ciphertexts[i]
        k = recover_one_key(u, x, A, B, C)
        print("Recovered key:", k)

        # Explore "close" key values
        for delta in range(-1, 2):  # Example: small perturbations
            k_candidate = (k + delta) % p
            x_test = encryption(u, k_candidate)
            if np.array_equal(x_test, x):
                print("Exact key found:", k_candidate)
                break

# Define the filepath to the file containing plaintext-ciphertext pairs
filepath = "KPAdataH_CyberDucks/KPAdataH/KPApairsH_nearly_linear.txt"
# Read the plaintext-ciphertext pairs from the file
plaintexts, ciphertexts = read_pairs_from_file(filepath)
find_keys(plaintexts, ciphertexts)