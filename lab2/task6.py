
import numpy as np
from collections import Counter
from task3 import decoder
from task2 import encoder
from task3 import convert_array_to_string
from task4 import convert_to_data_frame, plot_empirical_distribution, compute_distributions, compute_mutual_information_and_entropy
from task5 import bsc, number_of_errors
#from scipy.stats import entropy

def compute_error_probability(u, u_hat):
    return np.mean(u != u_hat)

def total_variation_distance(p, q):
    """Compute Total Variation Distance between two distributions."""
    return 0.5 * np.sum(np.abs(p - q))

def calculate_empirical_distribution_with_bsc(all_possible_input, iterations, delta):
    input_output_numbers_map = Counter()

    for u in all_possible_input:
        for _ in range(iterations):
            t = bsc(encoder(u), delta)

            input_output_numbers_map[(convert_array_to_string(u), convert_array_to_string(t))] += 1

    return input_output_numbers_map


def main():
    # 6.1 Setup
    #all possible 3 bit binary inputs
    all_possible_input = [list(tupla) for tupla in itertools.product([0, 1], repeat=3)]
    iterations = 1000  # Number of iterations for the simulation
    INPUT_LENGTH = 10  # Define the input length
    u = np.random.randint(0, 2, INPUT_LENGTH)
    x = encoder(u)

    epsilon_delta_pairs = [(0.01, 0.45), (0.05, 0.4), (0.1, 0.35), (0.15, 0,30), (0.20, 0.25)]

    results = []

    for epsilon, delta in epsilon_delta_pairs:
        print(f"\nFor epsilon={epsilon} and delta={delta}")

        # 6.1.a Repeat the simulations in Tasks 3 with the wiretap BSC
        # Simulate Bob's observations
        y = bsc(x, epsilon)
        u_hat = decoder(y)
        n = number_of_errors(u, u_hat)
        print(f"Bob's numbers of error with epsilon={epsilon}: {number_of_errors}")
        # 6.2 Evaluate the resulting reliability in terms of Bob's error rate
        error_prob = compute_error_probability(u, u_hat)
        print(f"Bob's Error Probability with epsilon={epsilon}: {error_prob}")

        # 6.1.b Repeat the simulations in Task 4 with the wiretap BSC

        # 6.3
        # Simulate Eve's observations
        input_output_numbers_map = calculate_empirical_distribution_with_bsc(all_possible_input, iterations, delta)
        df = convert_to_data_frame(input_output_numbers_map)
        plot_empirical_distribution(df)
        total_samples = len(all_possible_input) * iterations
        p_uz, p_u, p_z = compute_distributions(input_output_numbers_map, total_samples)
        I_u_z, H_u = compute_mutual_information_and_entropy(p_uz, p_u, p_z)
        print(f"Mutual Information (with delta={delta}) I(U;Z): {I_u_z:.6f}")
        print(f"Entropy (with delta={delta}) H(U): {H_u:.6f}")

        # 6.4 Compute the total variation distance
        joint_hist_real = np.histogram2d(u, u_hat, bins=2)[0]
        p_real = joint_hist_real.flatten() / np.sum(joint_hist_real)

        u_shuffled = np.random.permutation(u)
        joint_hist_ideal = np.histogram2d(u, u_shuffled, bins=2)[0]
        p_ideal = joint_hist_ideal.flatten() / np.sum(joint_hist_ideal)

        tvd = total_variation_distance(p_real, p_ideal)

        # Compute simple upper bound
        upper_bound = error_prob + leakage

        results.append({
            'epsilon': epsilon,
            'delta': delta,
            'error_prob': error_prob,
            'leakage': leakage,
            'tvd': tvd,
            'upper_bound': upper_bound
        })



if __name__ == "__main__":
    main()