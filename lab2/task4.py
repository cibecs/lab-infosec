import numpy as np
from task2 import encoder
from task1 import plot_statistic, MAX_ERRORS_CHANNEL, MAX_ERRORS_EAVESDROPPER, xor_between_vectors, NUM_BITS, generateAllErrors, getRandomElement

import itertools

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
import math

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

def convert_array_to_string(arr):
    return "".join(str(x) for x in arr)

def calculate_empirical_distribution(all_possible_input, iterations): 
    input_output_numbers_map = Counter()

    for u in all_possible_input:
        for _ in range(iterations):
            t = encoder_plus_channel_errors(u, MAX_ERRORS_EAVESDROPPER)

            input_output_numbers_map[(convert_array_to_string(u), convert_array_to_string(t))] += 1

    return input_output_numbers_map

def compute_distributions(joint_counts, total_samples):
    # Joint p(u,z)
    p_uz = {k: v / total_samples for k, v in joint_counts.items()}

    # Marginals
    p_u = defaultdict(float)
    p_z = defaultdict(float)
    for (u, z), p in p_uz.items():
        p_u[u] += p
        p_z[z] += p

    return p_uz, p_u, p_z

def compute_mutual_information_and_entropy(p_uz, p_u, p_z):
    I = 0.0  # Mutual information
    H_u = 0.0  # Entropy of U
    
    # Compute mutual information
    for (u, z), p_joint in p_uz.items():
        if p_joint > 0:
            I += p_joint * math.log2(p_joint / (p_u[u] * p_z[z]))
    
    # Compute entropy H(U)
    for u_val, p_val in p_u.items():
        if p_val > 0:
            H_u -= p_val * math.log2(p_val)
    
    return I, H_u

def plot_empirical_distribution(df):
    plt.figure(figsize=(22, 6))
    sns.heatmap(df, cmap="viridis", annot=False, )
    plt.xlabel("z (channel output)")
    plt.ylabel("u (original message)")
    plt.title("Empirical Conditional PMD: p̂(z | u)")
    plt.tight_layout()
    plt.show()

def convert_to_data_frame (data):
    df = pd.DataFrame(
    [(k[0], k[1], v) for k, v in data.items()],
    columns=["row", "col", "value"])
    heatmap_data = df.pivot(index="row", columns="col", values="value")

# Convert to float (important!)
    heatmap_data = heatmap_data.astype(float)
    return heatmap_data

def main():
    iterations = 100000
    input_output_numbers_map = calculate_empirical_distribution(all_possible_input, iterations)
    df = convert_to_data_frame(input_output_numbers_map)
    plot_empirical_distribution(df)
    total_samples = len(all_possible_input) * iterations
    p_uz, p_u, p_z = compute_distributions(input_output_numbers_map, total_samples)

    I_u_z, H_u = compute_mutual_information_and_entropy(p_uz, p_u, p_z)
    print(f"Mutual Information I(U;Z): {I_u_z:.6f}")
    print(f"Entropy H(U): {H_u:.6f}")

if __name__ == "__main__":
    main() 
