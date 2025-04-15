import numpy as np
from task2 import hamming
from task1 import xor_between_vectors

input = [1, 0, 1, 0, 1, 1, 1]

def minimum_distance_with_code(x, all_word_code):
    distances = {}
    for k in all_word_code:
        distance = 0
        if len(x) != len(k):
            raise ValueError("Array length should be equal")
        for i in range(len(x)):
            if x[i] != k[i]:
                distance += 1
        distances["".join(str(bit) for bit in k)] = distance

    return min(distances, key=distances.get)

def find_real_input(codeword):
    codeword = np.array([int(bit) for bit in codeword])
    if(codeword[0] == 0):
        return np.array(codeword[1:4])
    return np.array(xor_between_vectors(codeword[1:4], [1, 1, 1]))


def main():
    word = minimum_distance_with_code(input, hamming)
    word = find_real_input(word)
    print(word)

if __name__ == "__main__":
    main()