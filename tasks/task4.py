import numpy as np
from task3 import generate_matrix_A_B
from task1 import encryption, p
from task2 import modular_inverse_matrix

def recover_key(u, x, A, B):
    # Compute the modular inverse of matrix A modulo p
    A_inv = modular_inverse_matrix(A)
    # Compute the product of matrix B and vector u modulo p
    Bu = (B @ u) 
    # Compute the difference between the ciphertext x and Bu modulo p
    diff = (x - Bu) 
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
    return plaintexts, ciphertexts

def validateKey(plaintexts, ciphertexts, k):
    # Iterate over all plaintext-ciphertext pairs
    for i in range(len(plaintexts)):
        u = plaintexts[i]
        x = ciphertexts[i]
        # Compute the encryption of the plaintext u using the key k
        x_test = encryption(u, k)
        # Check if the computed ciphertext matches the given ciphertext
        if not np.array_equal(x, x_test):
            print("Test failed at index ", i)
            print("expected:" , x , "actual:" , x_test)
            return
    print("Test passed")

if __name__ == "__main__":
    # Generate the matrices A and B using the function from task3
    A, B = generate_matrix_A_B()

    # Define the filepath to the file containing plaintext-ciphertext pairs
    filepath = "KPAdataH_CyberDucks/KPAdataH/KPApairsH_linear.txt"
    # Read the plaintext-ciphertext pairs from the file
    plaintexts, ciphertexts = read_pairs_from_file(filepath)
    
    k = recover_key(plaintexts[0], ciphertexts[0], A, B)
    print(k)
        
    validateKey(plaintexts, ciphertexts, k) 
