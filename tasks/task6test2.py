from task1 import p
from task5 import encryption
from task2 import modular_inverse_matrix
from task4 import read_pairs_from_file
import numpy as np              

C = np.identity(8, dtype=int)  # Tentativo iniziale, ma può essere migliorato in seguito

def generate_matrix_A_B():
    dim = 8
    A_matrix = np.zeros((dim, dim), dtype=int)
    B_matrix = np.zeros((dim, dim), dtype=int)
    for j in range(dim):
        e_j = np.zeros(dim, dtype=int)
        e_j[j] = 1
        A_matrix[:, j] = encryption(np.zeros(dim, dtype=int), e_j)
        B_matrix[:, j] = encryption(e_j, np.zeros(dim, dtype=int))
    return A_matrix, B_matrix

def recover_one_key(u, x, A, B):
    A_inv = modular_inverse_matrix(A)
    Bu = B @ u
    Cx = C @ x
    diff = (Cx - Bu)
    k = (A_inv @ diff) % p
    return k

def find_keys(plaintexts, ciphertexts):
    A, B = generate_matrix_A_B()
    for i in range(len(plaintexts)):
        u = plaintexts[i]
        x = ciphertexts[i]
        k = recover_one_key(u, x, A, B)
        print("Key found:", k)

        total_hamming = compute_total_hamming(k, plaintexts, ciphertexts)
        print("Total Hamming Distance:", total_hamming)

def compute_total_hamming(key, plaintexts, ciphertexts):
    total_hamming = 0
    for i in range(len(plaintexts)):
        u = plaintexts[i]
        x_real = ciphertexts[i]
        x_test = encryption(u, key)
        total_hamming += np.sum(x_real != x_test)
    return total_hamming

def explore_nearby_keys(best_key, A, B, plaintexts, ciphertexts):
    dim = len(best_key)
    best_hd = float('inf')
    best_candidate = None

    for i in range(dim):
        for delta in range(1, p):
            for sign in [-1, 1]:
                new_key = best_key.copy()
                new_key[i] = (new_key[i] + sign * delta) % p
                total_hamming = compute_total_hamming(new_key, plaintexts, ciphertexts)

                if total_hamming < best_hd:
                    best_hd = total_hamming
                    best_candidate = new_key.copy()
                    print("Better key found:", best_candidate, "Hamming:", best_hd)

                if best_hd == 0:
                    return best_candidate
    return best_candidate

# 🔁 Nuova funzione di hill climbing multi-step
def hill_climb_key(initial_key, plaintexts, ciphertexts, max_iter=20):
    current_key = initial_key.copy()
    current_hd = compute_total_hamming(current_key, plaintexts, ciphertexts)

    for _ in range(max_iter):
        improved = False
        for i in range(len(current_key)):
            for delta in range(1, p):
                for sign in [-1, 1]:
                    test_key = current_key.copy()
                    test_key[i] = (test_key[i] + sign * delta) % p
                    test_hd = compute_total_hamming(test_key, plaintexts, ciphertexts)
                    if test_hd < current_hd:
                        print("Better key found:", test_key, "Hamming:", test_hd)
                        current_key = test_key
                        current_hd = test_hd
                        improved = True
        if not improved:
            break
    return current_key

# === MAIN SCRIPT ===
filepath = "KPAdataH_CyberDucks/KPAdataH/KPApairsH_nearly_linear.txt"
plaintexts, ciphertexts = read_pairs_from_file(filepath)

# Prima fase: prova con recover_one_key
find_keys(plaintexts, ciphertexts)

# Seconda fase: partendo dalla migliore chiave trovata
A, B = generate_matrix_A_B()
best_key = np.array([10, 1, 2, 3, 0, 8, 2, 10])  # Da output precedente
refined_key = explore_nearby_keys(best_key, A, B, plaintexts, ciphertexts)
print("Refined key after neighborhood search:", refined_key)

# Terza fase: hill climbing iterativo su chiave raffinata
final_key = hill_climb_key(refined_key, plaintexts, ciphertexts, max_iter=20)
final_hd = compute_total_hamming(final_key, plaintexts, ciphertexts)

print("Final candidate key:", final_key)
print("Final Hamming Distance:", final_hd)
