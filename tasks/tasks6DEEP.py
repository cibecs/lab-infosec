import numpy as np
from task5 import encryption

p = 11
substitution_map = {0: 0, 1: 2, 2: 4, 3: 8, 4: 6, 5: 10, 6: 1, 7: 3, 8: 5, 9: 7, 10: 9}

def substitution(v):
    return [substitution_map[vi] for vi in v]

def generate_matrix_A_B():
    dim = 8
    A = np.zeros((dim, dim), dtype=int)
    B = np.zeros((dim, dim), dtype=int)
    for j in range(dim):
        e_j = np.zeros(dim, dtype=int)
        e_j[j] = 1
        A[:, j] = encryption(np.zeros(dim, dtype=int), e_j)
        B[:, j] = encryption(e_j, np.zeros(dim, dtype=int))
    return A, B

def compute_true_matrix_C():
    """
    Compute the matrix C dynamically based on the cipher's behavior.
    """
    dim = 8
    C = np.zeros((dim, dim), dtype=int)
    for j in range(dim):
        # Create the unit vector e_j
        e_j = np.zeros(dim, dtype=int)
        e_j[j] = 1
        # Encrypt e_j with itself as the key to observe the effect on the ciphertext
        x = encryption(e_j, e_j)  # Use e_j as both the input and the key
        C[:, j] = x
    return C

def modular_inverse_matrix(A, p):
    det = int(np.round(np.linalg.det(A)))
    det_inv = pow(det, -1, p) if np.gcd(det, p) == 1 else None
    if det_inv is None:
        raise ValueError("Matrix is not invertible modulo p.")
    A_inv = (det_inv * np.round(np.linalg.inv(A) * det)).astype(int) % p
    return A_inv

def linear_cryptanalysis_attack(plaintexts, ciphertexts):
    A, B = generate_matrix_A_B()
    C = compute_true_matrix_C()  # Use the corrected C computation
    print("Matrix A:\n", A)
    print("Matrix B:\n", B)
    print("Matrix C:\n", C)

    # Test linear approximation
    total = len(plaintexts)
    successes = 0
    for u, x in zip(plaintexts, ciphertexts):
        k_random = np.random.randint(0, p, size=8)
        lhs = (A @ k_random + B @ u + C @ x) % p
        if np.all(lhs == 0):
            successes += 1
    probability = successes / total
    threshold = 1 / (p ** 8)
    print(f"Linear approximation probability: {probability} (Threshold: {threshold})")

    # Key recovery
    for u, x in zip(plaintexts, ciphertexts):
        try:
            A_inv = modular_inverse_matrix(A, p)
            k_candidate = (A_inv @ (C @ x - B @ u)) % p
            if np.array_equal(encryption(u, k_candidate), x):
                print("Exact key found:", k_candidate)
                return k_candidate
            else:
                print("Candidate key:", k_candidate)
                # Try small perturbations
                for delta in [np.zeros(8)] + [np.eye(8, dtype=int)[i] for i in range(8)]:
                    k_perturbed = (k_candidate + delta) % p
                    if np.array_equal(encryption(u, k_perturbed), x):
                        print("Exact key via perturbation:", k_perturbed)
                        return k_perturbed
        except ValueError:
            print("Matrix A not invertible for this pair. Skipping.")

    return None

# Example usage
if __name__ == "__main__":
    plaintexts = [
        np.array([0, 10, 3, 1, 3, 8, 6, 8]),
        np.array([8, 9, 6, 1, 6, 1, 7, 5]),
        np.array([8, 1, 2, 0, 10, 6, 5, 4]),
        np.array([3, 1, 10, 6, 6, 8, 7, 10]),
        np.array([10, 8, 7, 2, 5, 5, 8, 1]),
    ]
    ciphertexts = [
        np.array([2, 7, 6, 8, 1, 7, 9, 3]),
        np.array([0, 8, 8, 9, 10, 10, 1, 5]),
        np.array([2, 2, 3, 3, 2, 2, 3, 3]),
        np.array([10, 10, 2, 0, 4, 2, 10, 8]),
        np.array([3, 0, 9, 9, 0, 7, 10, 9]),
    ]
    recovered_key = linear_cryptanalysis_attack(plaintexts, ciphertexts)
    if recovered_key is not None:
        print("Successfully recovered key:", recovered_key)
    else:
        print("Key not found. Try more pairs or a different approach.")