import numpy as np
from task3 import generate_matrix_A_B  # Import the function from Task 3

# Define the field size (p) and dimensions
p = 11  # Field size (modulus)
l = 8   # Length of plaintext/ciphertext vectors (updated to match the data)
k_len = 8  # Length of the key

# Function to compute modular inverse of a matrix
def mod_inverse_matrix(matrix, mod):
    det = int(round(np.linalg.det(matrix))) % mod
    det_inv = pow(det, -1, mod)
    adjugate = np.round(det * np.linalg.inv(matrix)).astype(int) % mod
    return (det_inv * adjugate) % mod

# Linear cryptanalysis function
def linear_cryptanalysis(plaintexts, ciphertexts):
    # Generate matrices A and B using the function from Task 3
    A, B = generate_matrix_A_B()

    # Use C as the identity matrix
    C = np.eye(l, dtype=int)

    # Debugging: Print matrices A and B
    print("Matrix A:\n", A)
    print("Matrix B:\n", B)

    # Check if A is invertible
    if np.linalg.det(A) % p == 0:
        print("Matrix A is not invertible. Key recovery cannot proceed.")
        return None

    # Compute the key using the encryption formula
    keys = []
    for u, x in zip(plaintexts, ciphertexts):
        u = np.array(u)
        x = np.array(x)
        try:
            k = (mod_inverse_matrix(A, p) @ (x - B @ u)) % p
            keys.append(k)
        except np.linalg.LinAlgError:
            print("Matrix A is not invertible. Key recovery failed.")
            return None

    # Compute the most frequent key
    keys = np.array(keys)
    key = np.round(np.mean(keys, axis=0)).astype(int) % p

    # Debugging: Validate the encryption property
    for u, x in zip(plaintexts, ciphertexts):
        u = np.array(u)
        x = np.array(x)
        x_calculated = (A @ key + B @ u) % p
        print(f"Plaintext: {u}")
        print(f"Expected Ciphertext: {x}")
        print(f"Calculated Ciphertext: {x_calculated}")
        if not np.array_equal(x, x_calculated):
            print(f"Validation failed for plaintext {u}. Expected {x}, got {x_calculated}")

    return key

# Helper function to compute probability
def compute_probability(A, B, C, plaintexts, ciphertexts):
    count = 0
    for u, x in zip(plaintexts, ciphertexts):
        u = np.array(u)
        x = np.array(x)
        if np.all((A @ u + B @ u + C @ x) % p == 0):
            count += 1
    return count / len(plaintexts)

# Function to verify if the recovered key is correct
def verify_key(key, plaintexts, ciphertexts):
    for u, x in zip(plaintexts, ciphertexts):
        u = np.array(u)
        x = np.array(x)
        # Re-encrypt the plaintext using the recovered key
        re_encrypted = (key @ u) % p
        if not np.array_equal(re_encrypted, x):
            print("Key verification failed for plaintext:", u)
            return False
    return True

# Example usage
if __name__ == "__main__":

    # Load plaintext/ciphertext pairs from file
    plaintexts = [
        [0, 10, 3, 1, 3, 8, 6, 8],
        [8, 9, 6, 1, 6, 1, 7, 5],
        [8, 1, 2, 0, 10, 6, 5, 4],
        [3, 1, 10, 6, 6, 8, 7, 10],
        [10, 8, 7, 2, 5, 5, 8, 1]
    ]
    ciphertexts = [
        [2, 7, 6, 8, 1, 7, 9, 3],
        [0, 8, 8, 9, 10, 10, 1, 5],
        [2, 2, 3, 3, 2, 2, 3, 3],
        [10, 10, 2, 0, 4, 2, 10, 8],
        [3, 0, 9, 9, 0, 7, 10, 9]
    ]

    # Perform linear cryptanalysis
    key = linear_cryptanalysis(plaintexts, ciphertexts)
    print("Recovered key:", key)

    # Verify the recovered key
    if verify_key(key, plaintexts, ciphertexts):
        print("Key verification successful! The recovered key is correct.")
    else:
        print("Key verification failed. The recovered key is incorrect.")