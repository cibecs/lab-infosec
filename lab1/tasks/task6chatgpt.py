import numpy as np
from sympy import Matrix
from task1 import encryption

# === PARAMETRI ===
P = 11  # Campo finito
FILENAME = "KPAdataH_CyberDucks/KPAdataH/KPApairsH_nearly_linear.txt"  # <--- CAMBIA QUESTO!

# === STEP 1: CARICA COPPIE KNOWN PLAINTEXT ===
def load_kpa_pairs(filename):
    with open(filename) as f:
        lines = f.readlines()
        pairs = []
        for line in lines:
            parts = list(map(int, line.strip().split()))
            u = parts[:8]  # Plaintext
            x = parts[8:]  # Ciphertext
            pairs.append((u, x))
    return pairs

# === STEP 2: STIMA MATRICE B TALE CHE x ≈ Bu (mod p) ===
def estimate_B(pairs, p):
    U = []
    X = []
    for u, x in pairs:
        U.append(u)
        X.append(x)
    U = Matrix(U)       # (m x l_u)
    X = Matrix(X)       # (m x l_x)
    
    B = ((U.T * U).inv_mod(p) * U.T * X) % p
    return B.T  # Restituisce B con dimensione (l_x x l_u)

# === STEP 3: RECUPERO CHIAVE k ≈ x - Bu (mod p) ===
def recover_key(B, u, x, p):
    Bu = (B * Matrix(u)) % p
    k = (Matrix(x) - Bu) % p
    return list(map(int, k))

# === STEP 4: RICERCA LOCALE VICINO ALLA CHIAVE STIMATA ===
def local_key_search(k_guess, u, x_target, p, radius=1):
    from itertools import product

    ranges = [range(max(0, val - radius), min(p, val + radius + 1)) for val in k_guess]
    for candidate in product(*ranges):
        if encryption(u, list(candidate)) == x_target:
            return list(candidate)
    return None

# === MAIN ===
def main():
    pairs = load_kpa_pairs(FILENAME)

    # Usa tutte tranne una coppia per stimare
    B = estimate_B(pairs[:-1], P)
    
    # Ultima coppia per test
    u_test, x_test = pairs[-1]

    # Chiave stimata
    k_guess = recover_key(B, u_test, x_test, P)
    print("Chiave stimata:", k_guess)

    # Verifica se funziona subito
    x_recalc = encryption(u_test, k_guess)
    print("x ricostruito: ", x_recalc)
    print("x atteso:     ", x_test)

    if x_recalc == x_test:
        print("✅ La chiave stimata è corretta!")
    else:
        print("⚠️  Approssimazione non perfetta. Provo chiavi vicine...")
        k_close = local_key_search(k_guess, u_test, x_test, P, radius=1)
        if k_close:
            print("✅ Chiave trovata per esplorazione locale:", k_close)
        else:
            print("❌ Nessuna chiave vicina funziona. Aumenta il raggio di ricerca.")

if __name__ == "__main__":
    main()
