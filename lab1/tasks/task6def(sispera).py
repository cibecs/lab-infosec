import numpy as np
from task4 import read_pairs_from_file
from task5 import encryption
from task1 import p

# Generatore efficiente di varianti a distanza esatta
def varianti_lazy(chiave_base, distanza):
    len_chiave = len(chiave_base)  # Calcolo dinamico della lunghezza

    def backtrack(pos, current, restante):
        if pos == len_chiave:
            if restante == 0:
                yield (chiave_base + np.array(current)) % p
            return
        for delta in range(-restante, restante + 1):
            current[pos] = delta
            yield from backtrack(pos + 1, current, restante - abs(delta))

    current = [0] * len_chiave
    yield from backtrack(0, current, distanza)

# Funzione per testare se una chiave è valida su tutti i plaintext/ciphertext
def test_chiave(k, plaintexts, ciphertexts, encryption):
    if not np.array_equal(encryption(plaintexts[0], k), ciphertexts[0]):
        return False
    for u, x in zip(plaintexts, ciphertexts):
        if not np.array_equal(encryption(u, k), x):
            return False
    return True

# Brute force senza parallelizzazione, con stampa progressiva
def brute_force_da_chiave_base_lazy(chiave_base, plaintexts, ciphertexts, encryption, distanza_massima=5*8):
    for d in range(1, distanza_massima + 1):
        count = 0
        print(f"[+] Testing chiavi a distanza {d}")
        for chiave in varianti_lazy(chiave_base, d):
            count += 1
            if np.array_equal(chiave, np.array([5,10,4,9,2,3,3,8])):
                print("Sto testando la chiave giusta")
            if test_chiave(chiave, plaintexts, ciphertexts, encryption):
                print("[✓] Chiave trovata:", chiave)
                return chiave
        print(count, " chiavi testate a distanza", d)
    print("[-] Nessuna chiave valida trovata.")
    return None

# Define the filepath to the file containing plaintext-ciphertext pairs
filepath = "KPAdataH_CyberDucks/KPAdataH/KPApairsH_nearly_linear.txt"
# Read the plaintext-ciphertext pairs from the file
plaintexts, ciphertexts = read_pairs_from_file(filepath)
key = np.array([5,4,4,8,2,6,3,4])
brute_force_da_chiave_base_lazy(key, plaintexts, ciphertexts, encryption)
