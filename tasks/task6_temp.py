from task1 import p
from task5 import encryption as en5
from task1 import encryption as en1
from task2 import modular_inverse_matrix
from task4 import read_pairs_from_file

from task7 import modular_inverse

import numpy as np              

# Function to generate matrices A and B
def generate_matrix_A_B_C():
    dim = 8  # Dimension of the matrices
    # Initialize matrices A and B with zeros
    A_matrix = np.zeros((dim, dim), dtype=int)
    B_matrix = np.zeros((dim, dim), dtype=int)
    C_matrix = 10 * np.identity(8)

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
    return A_matrix, B_matrix, C_matrix

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

import itertools

def brute_force_key_multi_delta(initial_key, plaintexts, ciphertexts, delta_range=p-1):
    """
    Funzione di brute-force che esplora modifiche simultanee su più valori della chiave
    e mostra il progresso in percentuale.
    """
    k = initial_key.copy()
    
    # Definisci il range di variazioni per ogni valore della chiave (puoi modificarlo a tuo piacere)
    deltas = list(range(-delta_range, delta_range + 1))
    
    # Creiamo tutte le combinazioni di delta per ogni valore della chiave
    delta_combinations = list(itertools.product(deltas, repeat=len(k)))
    
    total_combinations = len(delta_combinations)  # Numero totale di combinazioni
    print(f"Total combinations to test: {total_combinations}")
    
    # Prova tutte le combinazioni di delta
    for idx, delta_combo in enumerate(delta_combinations):
        modified_key = (np.array(k) + np.array(delta_combo)) % p
        
        # Controlla se questa combinazione genera ciphertext corretti
        all_correct = True
        for j in range(len(plaintexts)):
            if not np.array_equal(en5(plaintexts[j], modified_key), ciphertexts[j]):
                all_correct = False
                break
        
        # Stampa il progresso
        if idx % 100 == 0:  # Ogni 100 combinazioni stampiamo il progresso
            progress = (idx / total_combinations) * 100
            print(f"Progress: {progress:.2f}% ({idx}/{total_combinations})")
        
        if all_correct:
            print(f"Key found at combination {idx}/{total_combinations} ({(idx / total_combinations) * 100:.2f}%)")
            return modified_key  # Se la combinazione è corretta, restituisci la chiave

    print("Brute force completed, no valid key found.")
    return None  # Se nessuna combinazione è corretta

def find_keys(plaintexts, ciphertexts):
    A, B, C = generate_matrix_A_B_C()
    # Print the matrices A, B, and C
    print("Matrix A:\n", A)
    print("Matrix B:\n", B)
    print("Matrix C:\n", C)

    #trovo la chiave del primo plaintext-ciphertext
    k = []
    for i in range(len(plaintexts)):
        u = plaintexts[i]
        x = ciphertexts[i]
        k.append(recover_one_key(u, x, A, B, C))
        print("Key found:", k[i])


    num_keys = len(k)  # Numero di vettori in k
    key_length = len(k[0])  # Lunghezza di ciascun vettore (8 in questo caso)

    # Creiamo una lista per le medie
    averages = []

    # Calcoliamo la media per ogni indice j (0, 1, ..., 7)
    for j in range(key_length):
        avg = sum(k[i][j] for i in range(num_keys)) / num_keys
        averages.append(round(avg))    
    k = averages
    print("Initial key approximation:", k)

    refined_key = brute_force_key_multi_delta(k, plaintexts, ciphertexts)
    if refined_key is not None:
        print("Refined key found:", refined_key)
    else:
        print("Failed to find the correct key.")
        
# Define the filepath to the file containing plaintext-ciphertext pairs
filepath = "KPAdataH_CyberDucks/KPAdataH/KPApairsH_nearly_linear.txt"
# Read the plaintext-ciphertext pairs from the file
plaintexts, ciphertexts = read_pairs_from_file(filepath)
find_keys(plaintexts, ciphertexts)