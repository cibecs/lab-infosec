#import numpy as np
# AES-like cipher
#n = 5 # Number of rounds
#x = np.array([4, 0, 0, 9, 7, 0, 0, 3]) # Example input vector
#k = np.zeros(8) # Example key vector

import numpy as np
from task1 import subkey_generation, subkey_sum, substitution, transposition, linear, p, n

# Encryption function for the AES-like cipher
def encryption(k, u):
    # Generate subkeys from the main key
    subkey = subkey_generation(k)
    # Initialize the input vector
    w = u.copy()
    # Perform n rounds of encryption
    for i in range(n):
        # Add the subkey to the current state
        v = subkey_sum(w, subkey[i])
        # Apply the substitution step
        y = substitution(v)
        # Apply the transposition step
        z = transposition(y)
        # Apply the linear transformation if not the last round
        if i != n - 1:
            w = linear(z)
    # Add the final subkey to the state
    x = subkey_sum(z, subkey[n])
    # Return the result modulo p
    return x % p

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
        A_matrix[:, j] = encryption(k, u)

    # Compute matrix B: E(0, e_j)
    for j in range(dim):
        # Create the unit vector e_j
        e_j = np.zeros(dim, dtype=int)
        e_j[j] = 1
        # Use a zero vector as the key and e_j as the input
        k = np.zeros(dim, dtype=int)
        u = e_j
        # Encrypt and store the result in the j-th column of B
        B_matrix[:, j] = encryption(k, u)

    # Return the computed matrices A and B
    return A_matrix, B_matrix

# Execute the function and print the results
A, B = generate_matrix_A_B()
print("Matrix A:")
print(A)
print("\nMatrix B:")
print(B)
