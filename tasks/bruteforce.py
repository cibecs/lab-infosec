from itertools import product
from task5Andrea import encryption

# Lista di coppie (plaintext, ciphertext)
pairs = [
    ([0,10,3,1,3,8,6,8], [2,7,6,8,1,7,9,3]),
    ([8,9,6,1,6,1,7,5], [0,8,8,9,10,10,1,5]),
    ([8,1,2,0,10,6,5,4], [2,2,3,3,2,2,3,3]),
    ([3,1,10,6,6,8,7,10], [10,10,2,0,4,2,10,8]),
    ([10,8,7,2,5,5,8,1], [3,0,9,9,0,7,10,9])
]

total_keys = 11**8
progress_interval = total_keys // 20  # 5% step
count = 0

for k in product(range(11), repeat=8):
    if all(list(encryption(p, k)) == c for p, c in pairs):
        print("Chiave trovata:", list(k))
        break
    count += 1
    if count % progress_interval == 0:
        percent = (count * 100) // total_keys
        print(f"Progresso: {percent}% completato...")
else:
    print("Nessuna chiave trovata.")

