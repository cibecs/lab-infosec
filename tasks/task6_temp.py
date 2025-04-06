from task1 import p
from task5 import encryption as en5
from task1 import encryption as en1
from task2 import modular_inverse_matrix
from task4 import read_pairs_from_file

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
        A_matrix[:, j] = en1(u, k)

    # Compute matrix B: E(0, e_j)
    for j in range(dim):
        # Create the unit vector e_j
        e_j = np.zeros(dim, dtype=int)
        e_j[j] = 1
        # Use a zero vector as the key and e_j as the input
        k = np.zeros(dim, dtype=int)
        u = e_j
        # Encrypt and store the result in the j-th column of B
        B_matrix[:, j] = en1(u, k)

    # Return the computed matrices A and B
    return A_matrix, B_matrix

def recover_one_key(u, x, A, B, C):
    # Compute the modular inverse of matrix A 
    A_inv = modular_inverse_matrix(A)
    # Compute the product of matrix B and vector u 
    Bu = (B @ u) 
    # Compute the product of matrix C and vector x
    Cx = (C @ x) 
    # Compute the difference between the Cx and Bu 
    diff = (Cx - Bu) 
    # Compute the key k using the formula: k = A_inv @ diff % p
    k = (A_inv @ diff) % p
    return k

def key_approssimation(A, B, C, plaintexts, ciphertexts):
    #trovo la chiave del primo plaintext-ciphertext
    k = []
    for i in range(len(plaintexts)):
        u = plaintexts[i]
        x = ciphertexts[i]
        k.append(recover_one_key(u, x, A, B, C))
        #print("Key found:", k[i])

    num_keys = len(k)  # Numero di vettori in k
    key_length = len(k[0])  # Lunghezza di ciascun vettore (8 in questo caso)

    # Creiamo una lista per le medie
    averages = []
    # Calcoliamo la media per ogni indice j (0, 1, ..., 7)
    for j in range(key_length):
        avg = sum(k[i][j] for i in range(num_keys)) / num_keys
        averages.append(round(avg))    
    return averages

def find_keys(plaintexts, ciphertexts):
    A, B = generate_matrix_A_B()
    C = 10 * np.identity(8)  # Matrice C di partenza
    # Print the matrices A, B, and C
    print("Matrix A:\n", A)
    print("Matrix B:\n", B)
    print("Initial Matrix C:\n", C)

    k = key_approssimation(A, B, C, plaintexts, ciphertexts)
    # Stampa la chiave trovata 
    print("Key found: ", k)

    # Affina la chiave con il brute force 
    brute_force_da_chiave_base(k, plaintexts, ciphertexts)


from itertools import product

def genera_varianti(chiave_base, distanza):
    varianti = set()
    for distanza in range(1, distanza + 1):
        # Tutte le possibili variazioni tra -distanza e +distanza su 8 posizioni
        for delta in product(range(-distanza, distanza + 1), repeat=8):
            if sum(abs(x) for x in delta) != distanza:
                continue  # salta quelli non a distanza esatta
            nuova = (chiave_base + np.array(delta)) % p
            varianti.add(tuple(nuova))
    return [np.array(k) for k in varianti]

def varianti_lazy(chiave_base, distanza):
    for delta in product(range(-distanza, distanza + 1), repeat=8):
        if sum(abs(x) for x in delta) != distanza:
            continue
        yield (chiave_base + np.array(delta)) % p

def brute_force_da_chiave_base(chiave_base, plaintexts, ciphertexts):
    for d in range(1, 8 + 1):
        print(f"[+] Testing chiavi a distanza {d}")
        for k in varianti_lazy(chiave_base, d):
            # Primo test
            x_test = en5(plaintexts[0], k)
            if not np.array_equal(ciphertexts[0], x_test):
                continue  # Fallisce subito

            for u, x in zip(plaintexts, ciphertexts):
                if not np.array_equal(en5(u, k), x):
                    break  # Errore → scarta
            else:
                # Se arriva qui ha passato tutti i test
                print("[✓] Chiave trovata:", k)
                return k
    
    print("[-] Nessuna chiave valida trovata.")
    return None

# Define the filepath to the file containing plaintext-ciphertext pairs
filepath = "KPAdataH_CyberDucks/KPAdataH/KPApairsH_nearly_linear.txt"
# Read the plaintext-ciphertext pairs from the file
plaintexts, ciphertexts = read_pairs_from_file(filepath)
find_keys(plaintexts, ciphertexts)
