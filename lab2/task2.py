import numpy as np 
from task1 import xor_between_vectors, getRandomElement, NUM_BITS, generateAllErrors

u = [0, 0, 0]

binary_strings = [
    "0000000", "1000110", "0100101", "0010011",
    "0001111", "1100011", "1010101", "1001001",
    "0110110", "0101010", "0011100", "1110000",
    "1101100", "1011010", "0111001", "1111111"
]

# Convertiamo ogni stringa in una lista di interi (0 o 1)
hamming = [[int(bit) for bit in code] for code in binary_strings]

def generate_codewords(u):
    u = [0] + u
    for i in hamming:
        if i[:4] == u:
            # the first elemnet is the prefix 
            return np.array([i, xor_between_vectors(i, [1,1,1,1,1,1,1])])
    return None, None

def main():
    t = getRandomElement(generate_codewords(u))
    print(t)

if __name__ == "__main__":
    main()