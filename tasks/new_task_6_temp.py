import numpy as np
from itertools import product
from concurrent.futures import ProcessPoolExecutor, as_completed
from task4 import read_pairs_from_file
from task5 import encryption

p = 11
n = 8

def varianti_lazy(chiave_base, distanza):
    for delta in product(range(-distanza, distanza + 1), repeat=n):
        if sum(abs(x) for x in delta) != distanza:
            continue
        yield (chiave_base + np.array(delta)) % p

def test_chiave(k, plaintexts, ciphertexts, encryption):
    if not np.array_equal(encryption(plaintexts[0], k), ciphertexts[0]):
        return False
    for u, x in zip(plaintexts, ciphertexts):
        if not np.array_equal(encryption(u, k), x):
            return False
    return True

def brute_force_da_chiave_base_lazy_parallel(chiave_base, plaintexts, ciphertexts, encryption, distanza_massima=8, batch_size=100):
    tested = 0
    for d in range(1, distanza_massima + 1):
        print(f"[+] Testing chiavi a distanza {d}")
        batch = []
        for chiave in varianti_lazy(chiave_base, d):
            batch.append(chiave)
            if len(batch) >= batch_size:
                result = process_batch(batch, plaintexts, ciphertexts, encryption)
                tested += len(batch)
                print(f"  - Chiavi testate finora: {tested}")
                if result is not None:
                    print("[✓] Chiave trovata:", result)
                    return result
                batch = []
        # Testa eventuale batch finale rimasto
        if batch:
            result = process_batch(batch, plaintexts, ciphertexts, encryption)
            tested += len(batch)
            print(f"  - Chiavi testate finora: {tested}")
            if result is not None:
                print("[✓] Chiave trovata:", result)
                return result
    print("[-] Nessuna chiave valida trovata.")
    return None

def process_batch(batch, plaintexts, ciphertexts, encryption):
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(test_chiave, k, plaintexts, ciphertexts, encryption) for k in batch]
        for i, (fut, k) in enumerate(zip(as_completed(futures), batch)):
            if fut.result():
                return k  # Appena ne troviamo una buona, la restituiamo
    return None


if __name__ == '__main__':
    # Define the filepath to the file containing plaintext-ciphertext pairs
    filepath = "KPAdataH_CyberDucks/KPAdataH/KPApairsH_nearly_linear.txt"
    # Read the plaintext-ciphertext pairs from the file
    plaintexts, ciphertexts = read_pairs_from_file(filepath)

    chiave_base = np.array([5,4,2,0,6,0,1,4])

    chiave = brute_force_da_chiave_base_lazy_parallel(chiave_base, plaintexts, ciphertexts, encryption)    

    if chiave is not None:
        print("🔐 Chiave finale trovata:", chiave)
    else:
        print("❌ Nessuna chiave trovata.")