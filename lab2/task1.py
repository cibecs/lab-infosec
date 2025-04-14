import numpy as np

import itertools
import matplotlib.pyplot as plt

#improves the printing of arrays
np.set_printoptions(legacy='1.25')

a = [1, 0, 0, 1, 0, 0, 0] #input 

#generates all possible combinations of errors within a binary array of length num_bits
def generateAllErrors(num_bits, max_errors):
    if max_errors > num_bits or max_errors < 1:
        raise ValueError("max_errors must be between 1 and num_bits inclusive.")

    error_patterns =[]    
    for error_count in range(0, max_errors + 1):
        for positions in itertools.combinations(range(num_bits), error_count):
            error = [0] * num_bits
            for pos in positions:
                error[pos] = 1
            error_patterns.append(error)

    return np.array(error_patterns)

#returns a random element of a vector
def getRandomElement(vector):
    return vector[np.random.randint(len(vector))]

#applies a xor between two vectors of same length   
def xor_between_vectors(a, b):
    if len(a) != len(b):
        raise ValueError("Array length should be equal")
    result = [x ^ y for x, y in zip(a, b)]
    return result 

def edit_distance_between_vectors(a, b):
    distance = 0
    if len(a) != len(b):
        raise ValueError("Array length should be equal")
    for i in range (len(a)):
        if a[i] != b[i]:
            distance += 1
    return distance

def validateIndependency(x, iterations, num_bits, max_errors_channel, max_errors_eavesdropper):
    all_channel_errors = generateAllErrors(num_bits, max_errors_channel)
    all_eavesdropper_errors = generateAllErrors(num_bits, max_errors_eavesdropper)
    errors_channel = {i: 0 for i in range(num_bits + 1)}  # Initialize for all possible edit distances
    errors_eavesdropper = {i: 0 for i in range(num_bits + 1)}  # Initialize for all possible edit distances

    for i in range(iterations):
        b = getRandomElement(all_channel_errors)
        c = getRandomElement(all_eavesdropper_errors)
        y = xor_between_vectors(x, b)
        errors_channel[edit_distance_between_vectors(x, y)] += 1
        z = xor_between_vectors(x, c)
        errors_eavesdropper[edit_distance_between_vectors(x, z)] += 1
    
    return errors_channel, errors_eavesdropper

 

#histogram errors for the channel and eavesdropper
def plot_statistic(input_label, num_bits, errors):
    # Calcola il numero di errori possibili per ogni bit
    possible_errors = {i: len(list(itertools.combinations(range(num_bits), i))) for i in range(num_bits + 1)}

    # Crea un istogramma
    plt.bar(possible_errors.keys(), possible_errors.values(), label="Possibili errori", color="blue")
    plt.ylim(0, max(possible_errors.values()) + 1)
    plt.xticks(range(len(possible_errors)), possible_errors.keys())
    plt.legend()
    plt.ylabel("Numero di errori possibili")
    plt.xlabel("Numero di bit errati")
    plt.title(f"Istogramma degli errori possibili: {input_label}")
    plt.grid()
    plt.show()

def main():
    num_bits = 7  # Lunghezza del vettore
    errors_channel, errors_eavesdropper = validateIndependency(a, 10, num_bits, 1, 3)
    plot_statistic("Channel", num_bits, errors_channel)
    plot_statistic("Eavesdropper", num_bits, errors_eavesdropper)

if __name__ == "__main__":
    main()


