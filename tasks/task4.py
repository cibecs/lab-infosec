import numpy as np
from task3 import generate_matrix_A_B, p

# Function to compute the modular inverse of a matrix A modulo p
def modular_inverse_matrix(A, p):
    # Compute the determinant of the matrix A modulo p
    det = int(round(np.linalg.det(A))) % p
    # Compute the modular inverse of the determinant modulo p
    det_inv = pow(det, -1, p)
    # Compute the modular inverse of the matrix A using the formula:
    # A_inv = (det_inv * adj(A)) % p, where adj(A) is the adjugate matrix
    A_inv = np.round(det_inv * np.linalg.inv(A) * det).astype(int) % p
    return A_inv

# Function to recover the encryption key k given a plaintext u, ciphertext x, and matrices A and B
def recover_key(x, u, A, B):
    # Compute the modular inverse of matrix A modulo p
    A_inv = modular_inverse_matrix(A, p)
    # Compute the product of matrix B and vector u modulo p
    Bu = (B @ u) % p
    # Compute the difference between the ciphertext x and Bu modulo p
    diff = (x - Bu) % p
    # Compute the key k using the formula: k = A_inv @ diff % p
    k = (A_inv @ diff) % p
    return k

# Function to read plaintext-ciphertext pairs from a file
def read_pairs_from_file(filepath):
    # Open the file at the given filepath in read mode
    with open(filepath, 'r') as f:
        # Read all lines from the file, stripping whitespace and ignoring empty lines
        lines = [line.strip() for line in f if line.strip()]

    # Initialize empty lists to store plaintexts and ciphertexts
    plaintexts, ciphertexts = [], []
    for line in lines:
        try:
            # Remove square brackets from the line
            line = line.replace('[', '').replace(']', '')
            # Split the line into two parts: plaintext (left) and ciphertext (right)
            left, right = line.split()  # Separate plaintext and ciphertext
            # Convert the plaintext (left) into a NumPy array of integers
            u = np.array(list(map(int, left.split(','))))
            # Convert the ciphertext (right) into a NumPy array of integers
            x = np.array(list(map(int, right.split(','))))
            # Append the plaintext and ciphertext to their respective lists
            plaintexts.append(u)
            ciphertexts.append(x)
        except Exception as e:
            # Print an error message if there is an issue parsing the line
            print(f"Error parsing the line: {line}")
            print(e)

    # Return the lists of plaintexts and ciphertexts
    return plaintexts, ciphertexts


if __name__ == "__main__":
    # Generate the matrices A and B using the function from task3
    A, B = generate_matrix_A_B()

    # Define the filepath to the file containing plaintext-ciphertext pairs
    filepath = "KPAdataH_CyberDucks/KPAdataH/KPApairsH_linear.txt"
    # Read the plaintext-ciphertext pairs from the file
    plaintexts, ciphertexts = read_pairs_from_file(filepath)

    # Use the first plaintext-ciphertext pair (u, x) for key recovery
    u = plaintexts[0]
    x = ciphertexts[0]

    # Recover the encryption key k using the recover_key function
    k = recover_key(x, u, A, B)
    # Print the recovered key
    print("Recovered key k:")
    print(k)


from task1 import subkey_generation, subkey_sum, substitution, transposition, linear, n

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

# Test della chiave trovata su tutte le coppie
correct = 0
for i in range(len(plaintexts)):
    u_i = plaintexts[i]
    expected_x = ciphertexts[i]
    computed_x = encryption(k, u_i)
    if np.array_equal(computed_x, expected_x):
        correct += 1
    else:
        print(f"❌ Mismatch alla riga {i}:")
        print(f"u = {u_i}")
        print(f"x atteso = {expected_x}")
        print(f"x ottenuto = {computed_x}\n")

print(f"\n✅ La chiave trovata funziona su {correct}/{len(plaintexts)} coppie.")

