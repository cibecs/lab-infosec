import numpy as np
import sympy
from task1 import p
from task5 import encryption
from task2 import modular_inverse_matrix
from task4 import read_pairs_from_file
from task7 import modular_inverse

def generate_matrix_A_B_C(dim=8, p=11):
    A_matrix = np.zeros((dim, dim), dtype=int)
    B_matrix = np.zeros((dim, dim), dtype=int)
    C_matrix = np.zeros((dim, dim), dtype=int)
    
    for j in range(dim):
        e_j = np.zeros(dim, dtype=int)
        e_j[j] = 1
        k = e_j
        u = np.zeros(dim, dtype=int)
        A_matrix[:, j] = encryption(u, k)
    
    for j in range(dim):
        e_j = np.zeros(dim, dtype=int)
        e_j[j] = 1
        k = np.zeros(dim, dtype=int)
        u = e_j
        B_matrix[:, j] = encryption(u, k)
    
    num_samples = dim
    X = np.zeros((num_samples, dim), dtype=int)
    AX_BU = np.zeros((num_samples, dim), dtype=int)
    
    for i in range(num_samples):
        u = np.random.randint(0, p, size=dim)
        k = np.random.randint(0, p, size=dim)  

        x = encryption(u, k)
        
        X[i, :] = x
        AX_BU[i, :] = (-np.mod(A_matrix @ k + B_matrix @ u, p))
    
    X_sym = sympy.Matrix(X)
    AX_BU_sym = sympy.Matrix(AX_BU)
    
    try:
        X_inv = X_sym.inv_mod(p)
        C_matrix = (X_inv @ AX_BU_sym) % p
    except:
        C_matrix = np.eye(dim, dtype=int)  # Default to identity if non-invertible
    
    return A_matrix, B_matrix, np.array(C_matrix).astype(int)

def recover_one_key(u, x, A, B, C):
    try:
        A_inv = sympy.Matrix(A).inv_mod(p)
    except:
        return None  # Return None if A is not invertible
    
    Bu = (B @ u) % p
    Cx = (C @ x) % p
    diff = (Cx - Bu) % p
    k = (A_inv @ sympy.Matrix(diff)) % p
    return np.array(k).astype(int).flatten()

def find_keys(plaintexts, ciphertexts):
    A, B, C = generate_matrix_A_B_C()
    print("Matrix A:\n", A)
    print("Matrix B:\n", B)
    print("Matrix C:\n", C)
    
    best_key = None
    best_score = 0
    
    for i in range(len(plaintexts)):
        u = plaintexts[i]
        x = ciphertexts[i]
        k = recover_one_key(u, x, A, B, C)
        if k is None:
            continue
        
        score = 0
        for j in range(len(plaintexts)):
            u_current = plaintexts[j]
            x_current = ciphertexts[j]
            x_test = encryption(u_current, k)
            if np.array_equal(x_current, x_test):
                score += 1
        
        if score > best_score:
            best_score = score
            best_key = k
    
    print("Best key found:", best_key)
    print("Confidence score:", best_score / len(plaintexts))

filepath = "KPAdataH_CyberDucks/KPAdataH/KPApairsH_nearly_linear.txt"
plaintexts, ciphertexts = read_pairs_from_file(filepath)
find_keys(plaintexts, ciphertexts)