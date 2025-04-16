import numpy as np
from task2 import generate_codewords
from task1 import plot_statistic, MAX_ERRORS_CHANNEL, MAX_ERRORS_EAVESDROPPER, xor_between_vectors, NUM_BITS, generateAllErrors, getRandomElement

import itertools

all_possible_input = [list(tupla) for tupla in itertools.product([0, 1], repeat=3)]

def encoder_plus_channel_errors(u, max_error):
    codeword = getRandomElement(generate_codewords(u))
    if codeword is None:
        raise ValueError("No valid codeword found for the given input.")
    # Generate all possible error patterns
    error = getRandomElement(generateAllErrors(NUM_BITS, max_error))
    # Apply errors to the codewords
    codeword_with_errors = xor_between_vectors(codeword, error)
    return np.array(codeword_with_errors)

def empirical_distribution_of_z(all_possible_input, iterations):
    for u in all_possible_input:
        all_possible_codewords_with_channel_errors  = {
                                                   "".join(str(bit) for bit in i): 0 for i 
                                                   in [list(tupla) for tupla in itertools.product([0, 1], repeat=7)]
                                                   }
        for _ in range(iterations):
            t = encoder_plus_channel_errors(u, MAX_ERRORS_EAVESDROPPER)
            key = "".join(str(bit) for bit in t)
            all_possible_codewords_with_channel_errors[key] += 1
        
        plot_statistic(f"Empirical distribution of {u}", all_possible_codewords_with_channel_errors)

def main():
    empirical_distribution_of_z(all_possible_input, 10000)

if __name__ == "__main__":
    main() 
