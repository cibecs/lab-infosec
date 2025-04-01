import numpy as np
from task1 import encryption

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


# Execute the function and print the results
A, B = generate_matrix_A_B()
print("Matrix A:")
print(A)
print("\nMatrix B:")
print(B)
