import numpy as np
from task2 import encoder
from task1 import plot_statistic, MAX_ERRORS_CHANNEL, MAX_ERRORS_EAVESDROPPER, xor_between_vectors, NUM_BITS, generateAllErrors, getRandomElement

import itertools

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

#all possible 3 bit binary inputs
all_possible_input = [list(tupla) for tupla in itertools.product([0, 1], repeat=3)]

def encoder_plus_channel_errors(u, max_error):
    codeword = encoder(u)
    if codeword is None:
        raise ValueError("No valid codeword found for the given input.")
    # Generate all possible error patterns
    error = getRandomElement(generateAllErrors(NUM_BITS, max_error))
    # Apply errors to the codewords
    codeword_with_errors = xor_between_vectors(codeword, error)
    return np.array(codeword_with_errors)

def calculate_empirical_distribution(all_possible_input, iterations):
    all_z_strings = ["".join(seq) for seq in itertools.product("01", repeat=7)]
    distribution_matrix = []

    for u in all_possible_input:
        counts = {z: 0 for z in all_z_strings}
        for _ in range(iterations):
            t = encoder_plus_channel_errors(u, MAX_ERRORS_EAVESDROPPER)
            key = "".join(str(bit) for bit in t)
            counts[key] += 1

        total = sum(counts.values())
        row = [counts[z] / total for z in all_z_strings]
        distribution_matrix.append(row)

    df = pd.DataFrame(distribution_matrix,
                      index=["".join(str(bit) for bit in u) for u in all_possible_input],
                      columns=all_z_strings)
    return df

def plot_empirical_distribution(df):
    plt.figure(figsize=(22, 6))
    sns.heatmap(df, cmap="viridis", annot=False)
    plt.xlabel("z (channel output)")
    plt.ylabel("u (original message)")
    plt.title("Empirical Conditional PMD: p̂(z | u)")
    plt.tight_layout()
    plt.show()


def main():
    df = calculate_empirical_distribution(all_possible_input, 10000)
    plot_empirical_distribution(df)

if __name__ == "__main__":
    main() 
