import numpy as np
from task1 import encryption
from task2 import modular_inverse_matrix
from task4 import read_pairs_from_file
from task3 import generate_matrix_A_B

p = 11  # Modulus from Task 5
dim = 8  # Dimension of the vectors

# Generate matrices A and B

# Recover the key using the formula
def recover_key2(u, x, A, B):
    A_inv = modular_inverse_matrix(A)
    Bu = (u @ B) 
    C = np.eye(dim, dtype=int)  # Define C as an identity matrix
    Cx = (C @ x)  # Perform matrix-vector multiplication
    k = (A_inv @ (- Cx - Bu)) % p
    return k


def recover_keyC(u, x, A, B, C):
    """Recover the key using the formula k = A⁻¹(Cx - Bu) mod p"""
    A_inv = modular_inverse_matrix(A)
    u = u.flatten()  # Ensure u is a 1D vector
    x = x.flatten()  # Ensure x is a 1D vector
    assert x.shape[0] == C.shape[0], f"Shape mismatch: x {x.shape}, C {C.shape}"
    Cx = np.round((C @ x) % p).astype(int)  # C @ x mod p
    Bu = np.round((u @ B) % p).astype(int)  # u @ B mod p
    print(f"Cx dimensions: {Cx.shape}, Bu dimensions: {Bu.shape}")
    k = np.round((A_inv @ (-Cx - Bu)) % p).astype(int)  # A⁻¹(Cx - Bu) mod p
    return k

# Validate the recovered key
def validated_key(plaintexts, ciphertexts, k):
    for i in range(len(plaintexts)):
        u = plaintexts[i]
        x = ciphertexts[i]
        x_test = encryption(u, k)
        if not np.array_equal(x, x_test):
            print(f"Test failed for pair {i}")
            return
    print("All tests passed!")

# Step 1: Assume C is Identity Matrix (initial approximation)
def initial_C_identity(dim):
    return np.eye(dim, dtype=int)

def modular_inverse_matrix_mod_p(X, p):
    """Compute the modular inverse of a square matrix X modulo p."""
    det = int(np.round(np.linalg.det(X)))  # Compute determinant of X
    det_inv = pow(det, -1, p)  # Modular inverse of the determinant mod p
    adjugate = np.round(det * np.linalg.inv(X)).astype(int)  # Adjugate matrix
    X_inv = (det_inv * adjugate) % p  # Modular inverse of X
    return X_inv

def estimate_C(B, U, X, p):
    """Step 2: Solve for C in X C^T = (B U)^T mod p"""
    # Compute (B U)^T mod p
    U_B = (U @ B).T  # B @ U gives (B U), and .T transposes it
    #U_B = np.round(U_B).astype(int) % p  # Ensure integer values
    print("U_B :\n", U_B)

    # Compute the pseudo-inverse of X
    X_pseudo_inv = np.linalg.pinv(X)  # Compute pseudo-inverse of X
    X_pseudo_inv = np.round(X_pseudo_inv).astype(int) % p  # Ensure integer values and mod p
    print("X_pseudo_inv:\n", X_pseudo_inv)

    # Solve for C^T
    C_T = (X_pseudo_inv.T @ U_B) % p  # Solve for C^T mod p
    print("C Transposed:\n", C_T)

    # Transpose C^T to get C
    C = C_T.T % p
    print("Estimated C:\n", C)

    return C

def estimate_C_with_key(A, B, U, X, k, p):
    """Step 2: Solve for C in X C^T = (A k + B U)^T mod p"""
    # Compute (A k + B U)^T mod p
    Ak = np.round((A @ k) % p).astype(int)  # A @ k
    BU = np.round((B @ U.T) % p).astype(int)  # B @ U.T
    Ak_plus_BU = np.round((Ak[:, None] + BU) % p).astype(int)  # Add Ak to each column of BU
    print("Ak + BU:\n", Ak_plus_BU)

    # Compute the pseudo-inverse of X
    X_pseudo_inv = np.linalg.pinv(X)  # Compute pseudo-inverse of X
    X_pseudo_inv = np.round(X_pseudo_inv).astype(int) % p  # Ensure integer values and mod p
    print("X Pseudo-Inverse:\n", X_pseudo_inv)

    # Solve for C^T
    C_T = np.round((Ak_plus_BU.T @ X_pseudo_inv) % p).astype(int)  # Solve for C^T mod p
    print("C Transposed:\n", C_T)

    # Transpose C^T to get C
    C = np.round(C_T.T % p).astype(int)
    print("Estimated C:\n", C)

    return C

def validate_key(A, B, C, U, X, k, p):
    """Validates if the recovered key satisfies the equation for all pairs"""
    for i in range(U.shape[0]):
        left_side = (X[i] @ C.T) % p
        right_side = (A @ k + B @ U[i]) % p
        if not np.array_equal(left_side, right_side):
            return False
    return True


def recover_key_with_C(A, B, C, U, X, p):
    """Recover the key using the formula k = A⁻¹(.-Cx - Bu) mod p"""
    
    K = []
    for i in range(U.shape[0]):
        k=recover_keyC(U[i], X[i], A, B, C)
        #print(f"Pair {i}: Cx = {Cx}, Bu = {Bu}, k = {k}")
        K.append(k)
    return np.round(np.mean(K, axis=0)).astype(int)  # Compute the mean key and ensure integer values

def evaluate_C_bias(A, B, C, U, X, k, p):
    """Evaluates if P[A k + B u + C x ≡ 0 (mod p)] is significantly biased"""
    success_count = 0
    total = U.shape[0]
    
    for i in range(total):
        # Ensure X[i] is a 1D vector of shape (8,)
        x = X[i].flatten()  # Flatten to ensure it's a 1D vector
        assert x.shape[0] == C.shape[0], f"Shape mismatch: x {x.shape}, C {C.shape}"
        
        # Compute the left side of the equation
        left_side = (A @ k + B @ U[i] + C @ x) % p
        
        # Check if it's exactly 0 (mod p)
        if np.all(left_side == 0):
            success_count += 1

    # Compute observed probability
    observed_prob = success_count / total
    theoretical_prob = 1 / (p ** X.shape[1])  # p^l_x

    print(f"Observed Probability: {observed_prob:.6f}")
    print(f"Expected Random Probability: {theoretical_prob:.6f}")
    
    # Check if the observed probability is significantly higher than random guessing
    return observed_prob > theoretical_prob * 1.5  # Arbitrary threshold for significance

def recTheFuckyngK(A,B,C,U,X,p):
    """k = A⁻¹(.-Cx - Bu) mod p"""
    A_inv = modular_inverse_matrix(A)
    C_X = (C @ X.T)  # Perform matrix-vector multiplication
    B_U = (U @ B)
    k = (A_inv @ (- C_X - B_U)) % p
    return k

if __name__ == "__main__":
    # Read plaintext-ciphertext pairs
    filepath = "KPAdataH_CyberDucks/KPAdataH/KPApairsH_nearly_linear.txt"
    #plaintexts, ciphertexts = read_pairs_from_file(filepath)
    
    # Generate matrices A and B
    A, B = generate_matrix_A_B()

    #U = np.array(plaintexts)  # Convert plaintexts to numpy array
    #print("Plaintexts:\n", U)
    #X = np.array(ciphertexts)  # Convert ciphertexts to numpy array
    #print("Ciphertexts:\n", X)
    
    U = np.array([[0, 10, 3, 1, 3, 8, 6, 8],
                [8, 9, 6, 1, 6, 1, 7, 5],
                [8, 1, 2, 0, 10, 6, 5, 4],
                [3, 1, 10, 6, 6, 8, 7, 10],
                [10, 8, 7, 2, 5, 5, 8, 1]])
    X = np.array([[2, 7, 6, 8, 1, 7, 9, 3],
                [0, 8, 8, 9, 10, 10, 1, 5],
                [2, 2, 3, 3, 2, 2, 3, 3],
                [10, 10, 2, 0, 4, 2, 10, 8],
                [3, 0, 9, 9, 0, 7, 10, 9]])

    # Ensure X and U have the correct dimensions
    assert U.shape[1] == dim, f"U has incorrect dimensions: {U.shape}"
    assert X.shape[1] == dim, f"X has incorrect dimensions: {X.shape}"

    # Step 1: Initialize C as Identity Matrix
    C = initial_C_identity(8)

    # Step 2: Estimate C
    C = estimate_C(B, U, X, p)
    # Step 3: Recover key
    K = []
    for i in range(U.shape[0]):  # Iterate over all plaintext-ciphertext pairs
        k = recover_key2(U[i], X[i], A, B)  # Recover key for each pair
        print(f"Pair {i}: k = {k}")
        K.append(k)
    k2 = np.round(np.mean(K, axis=0)).astype(int)  # Compute the mean key and ensure integer values
    print(f"Mean k: {k2}")

    # Step 4: Refine C using the new key
    C = estimate_C_with_key(A, B, U, X, k2, p)
    #evaluate_C_bias(A, B, C, U, X, k2, p)
    # Step 5: Recover the new key
    k3 = recover_key_with_C(A, B, C, U, X, p)
    print(f"Refined Key: {k3}")

    k4 = recTheFuckyngK(A,B,C,U,X,p)
    print(f"Refined Key: {k4}")

    # Validate the recovered key
    is_valid = validate_key(A, B, C, U, X, k3, p)
    print("Is the refined key valid?", is_valid)
