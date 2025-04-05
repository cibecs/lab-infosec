import numpy as np
from task1 import encryption
from task2 import modular_inverse_matrix
from task4 import read_pairs_from_file
from task3 import generate_matrix_A_B

p = 11  # Modulus from Task 5
dim = 8  # Dimension of the vectors

# Recover the key using the formula:
# k = A^-1(-C*x - B*u) mod p
def recover_key(u, x, A, B, C, p):
    A_inv = modular_inverse_matrix(A)
    Bu = (B @ u) % p
    Cx = (C @ x) % p
    k = (A_inv @ (-Cx - Bu)) % p
    return k

# Validate the recovered key using the encryption function
def validated_key(plaintexts, ciphertexts, k):
    for i in range(len(plaintexts)):
        u = plaintexts[i]
        x = ciphertexts[i]
        x_test = encryption(u, k)
        if not np.array_equal(x, x_test):
            print(f"Test failed for pair {i}")
            return False
    print("All tests passed!")
    return True

# Step 1: Initialize C as Identity Matrix (initial approximation)
def initial_C_identity(dim):
    return np.eye(dim, dtype=int)

# Estimate C using the candidate key.
# We use the equation: X * C^T = (A*k + B*U)^T  mod p.
def estimate_C(B, U, X, A, k, p):
    # For each plaintext vector u, compute the right-hand side: A*k + B*u
    Y = np.array([ (A @ k + B @ u) % p for u in U ])
    # X is an array of ciphertexts.
    # We wish to solve for C in the system: X * C^T = Y.
    # Compute the pseudo-inverse of X (as floating point, then round and take mod p)
    X_pinv = np.linalg.pinv(X)
    # Solve for C^T and then transpose to get C.
    C_T = (np.round(X_pinv @ Y)) % p
    C = C_T.T % p
    return C

# Validate if the recovered key k and matrix C satisfy the relation for all pairs:
#   X[i] * C^T = A*k + B*U[i]  mod p.
def validate_key(A, B, C, U, X, k, p):
    for i in range(U.shape[0]):
        left_side = (X[i] @ C.T) % p
        right_side = (A @ k + B @ U[i]) % p
        if not np.array_equal(left_side, right_side):
            return False
    return True

if __name__ == "__main__":
    # Read plaintext-ciphertext pairs
    filepath = "KPAdataH_CyberDucks/KPAdataH/KPApairsH_nearly_linear.txt"
    plaintexts, ciphertexts = read_pairs_from_file(filepath)

    # Generate matrices A and B
    A, B = generate_matrix_A_B()

    U = np.array(plaintexts)  # Plaintexts as numpy array
    X = np.array(ciphertexts)  # Ciphertexts as numpy array
    
    # ---- Bootstrap process ----
    # Step 1: Initialize C as identity
    C = initial_C_identity(dim)

    # Step 2: Use initial C to recover candidate keys from all pairs.
    candidate_keys = []
    for i in range(U.shape[0]):
        k_candidate = recover_key(U[i], X[i], A, B, C, p)
        candidate_keys.append(k_candidate)
    # Average candidate keys (rounding to integers) to get a first candidate key.
    k_est = np.round(np.mean(candidate_keys, axis=0)).astype(int) % p
    print("Candidate key from initial recovery:\n", k_est)

    # Step 3: Re-estimate C using the candidate key.
    C = estimate_C(B, U, X, A, k_est, p)
    print("Re-estimated C:\n", C)

    # Optionally, one more iteration: recover keys with the new C.
    candidate_keys = []
    for i in range(U.shape[0]):
        k_candidate = recover_key(U[i], X[i], A, B, C, p)
        candidate_keys.append(k_candidate)
    k_est = np.round(np.mean(candidate_keys, axis=0)).astype(int) % p
    print("Refined candidate key:\n", k_est)

    # Validate that the key satisfies the relation on all pairs.
    valid_relation = validate_key(A, B, C, U, X, k_est, p)
    print("Does the recovered key satisfy the relation (X * C^T = A*k + B*u)?", valid_relation)

    # Validate the recovered key using encryption.
    if validated_key(plaintexts, ciphertexts, k_est):
        print("Final recovered key is valid!")
    else:
        print("Final recovered key is invalid.")
