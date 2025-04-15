import numpy as np 
from task1 import xor_between_vectors, getRandomElement

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
    print(hamming)
    for i in range(len(u)):
        if u[i] == 0:
            u.append(1)
        else:
            u.append(0)
    u = [0] + u
    print(u)
    for i in hamming:
        if i[:4] == u:
            return np.array([i, xor_between_vectors(i, [1,1,1,1,1,1,1])])
    return None, None

def take_codeword(t):
    return getRandomElement(t)


def main():
    t = generate_codewords(u)
    print(t)

if __name__ == "__main__":
    main()