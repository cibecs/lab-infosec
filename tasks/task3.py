import numpy as np
from task1 import encryption, p, u, k
    
dim = 8  # Dimension of the matrices

# Function to generate matrices A and B
def generate_matrix_A_B():
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

def validate_matrixs(A, B, u, k):
    # x = E(k, u) = Ak + Bu mod p
    x_true = encryption(u, k)
    x_calculated = (A @ k + B @ u) % p

    # Check if the encryption property holds
    if np.array_equal(x_true, x_calculated):
        print("Test passed")
    else:
        print("Test failed")

def main():
    # Execute the function and print the results
    A, B = generate_matrix_A_B()
    print("Matrix A:")
    print(A)
    print("\nMatrix B:")
    print(B)
    validate_matrixs(A, B, u, k)

if __name__ == "__main__":
    main()