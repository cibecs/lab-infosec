import numpy as np
from task1 import subkey_generation, subkey_sum, substitution, transposition, linear, p, n
from task3 import generate_matrix_A_B

def encryption(k, u):
    subkey = subkey_generation(k)
    w = u.copy()
    for i in range(n):
        v = subkey_sum(w, subkey[i])
        y = substitution(v)
        z = transposition(y)
        if i != n - 1:
            w = linear(z)
    x = subkey_sum(z, subkey[n])
    return x % p

def modular_inverse_matrix(A, p):
    det = int(round(np.linalg.det(A))) % p
    det_inv = pow(det, -1, p)
    A_inv = np.round(det_inv * np.linalg.inv(A) * det).astype(int) % p
    return A_inv

def recover_key(x, u, A, B):
    A_inv = modular_inverse_matrix(A, p)
    Bu = (B @ u) % p
    diff = (x - Bu) % p
    k = (A_inv @ diff) % p
    return k

def read_pairs_from_file(filepath):
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    plaintexts, ciphertexts = [], []
    for line in lines:
        try:
            line = line.replace('[', '').replace(']', '')
            left, right = line.split()
            u = np.array(list(map(int, left.split(','))))
            x = np.array(list(map(int, right.split(','))))
            plaintexts.append(u)
            ciphertexts.append(x)
        except Exception as e:
            print(f"Errore nel parsing della riga: {line}")
            print(e)

    return plaintexts, ciphertexts

if __name__ == "__main__":
    # Carica i dati
    filepath = "KPAdataH_CyberDucks/KPAdataH/KPApairsH_linear.txt"
    plaintexts, ciphertexts = read_pairs_from_file(filepath)

    # Matrici A e B
    A, B = generate_matrix_A_B()

    # Recupera la chiave dalla prima coppia
    u = plaintexts[0]
    x = ciphertexts[0]
    k = recover_key(x, u, A, B)

    print("Chiave recuperata:")
    print(k)

    # Testa su tutte le coppie
    print("\nVerifica della chiave su tutte le coppie:")
    correct = 0
    for i in range(len(plaintexts)):
        u_i = plaintexts[i]
        expected_x = ciphertexts[i]
        computed_x = encryption(k, u_i)
        if np.array_equal(computed_x, expected_x):
            correct += 1
        else:
            print(f"Errore alla coppia {i}:")
            print(f"u = {u_i}")
            print(f"x atteso = {expected_x}")
            print(f"x ottenuto = {computed_x}\n")

    print(f"\nLa chiave funziona su {correct}/{len(plaintexts)} coppie.")
