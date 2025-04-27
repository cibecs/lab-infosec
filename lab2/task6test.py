import numpy as np
import itertools
import matplotlib.pyplot as plt
from collections import Counter
from scipy.interpolate import griddata
from task3 import decoder
from task2 import encoder
from task3 import convert_array_to_string
from task4 import convert_to_data_frame, plot_empirical_distribution, compute_distributions, compute_mutual_information_and_entropy
from task5 import bsc, number_of_errors

def compute_error_probability(u, u_hat):
    return np.mean(u != u_hat)

def total_variation_distance(p, q):
    return 0.5 * np.sum(np.abs(p - q))

def calculate_empirical_distribution_with_bsc(all_possible_input, iterations, delta):
    input_output_numbers_map = Counter()

    for u in all_possible_input:
        for _ in range(iterations):
            t = bsc(encoder(u), delta)
            input_output_numbers_map[(convert_array_to_string(u), convert_array_to_string(t))] += 1

    return input_output_numbers_map

def main():
    # Setup
    all_possible_input = [list(tupla) for tupla in itertools.product([0, 1], repeat=3)]
    iterations = 1000
    INPUT_LENGTH = 10
    u = np.random.randint(0, 2, INPUT_LENGTH)
    x = encoder(u)

    epsilon_delta_pairs = [(0.01, 0.45), (0.05, 0.4), (0.1, 0.35), (0.15, 0.30), (0.20, 0.25)]

    results = []

    for epsilon, delta in epsilon_delta_pairs:
        print(f"\n==== Epsilon={epsilon} | Delta={delta} ====")

        # Bob's observations
        y = bsc(x, epsilon)
        u_hat = decoder(y)
        n = number_of_errors(u, u_hat)
        print(f"Bob's number of errors: {n}")

        error_prob = compute_error_probability(u, u_hat)
        print(f"Bob's Error Probability: {error_prob:.6f}")

        # Eve's observations
        input_output_numbers_map = calculate_empirical_distribution_with_bsc(all_possible_input, iterations, delta)
        df = convert_to_data_frame(input_output_numbers_map)
        plot_empirical_distribution(df)

        total_samples = len(all_possible_input) * iterations
        p_uz, p_u, p_z = compute_distributions(input_output_numbers_map, total_samples)
        I_u_z, H_u = compute_mutual_information_and_entropy(p_uz, p_u, p_z)
        leakage = I_u_z

        print(f"Mutual Information I(U;Z): {I_u_z:.6f}")
        print(f"Entropy H(U): {H_u:.6f}")

        # TVD calculation (between p_uz and p_u x p_z)
        p_u_z_product = np.outer(p_u, p_z).flatten()
        tvd = total_variation_distance(p_uz.flatten(), p_u_z_product)

        # Upper Bound
        upper_bound = error_prob + leakage

        print(f"TVD: {tvd:.6f}")
        print(f"Upper Bound (Error Prob + Leakage): {upper_bound:.6f}")

        if tvd <= upper_bound:
            print("✅ TVD is within the expected upper bound.")
        else:
            print("❌ Warning: TVD exceeds the upper bound!")

        results.append({
            'epsilon': epsilon,
            'delta': delta,
            'error_prob': error_prob,
            'leakage': leakage,
            'tvd': tvd,
            'upper_bound': upper_bound
        })

    # Plotting Results
    plot_results(results)

    # After running all experiments
    plot_error_probability_vs_epsilon(results)
    plot_mutual_information_vs_delta(results)
    plot_security_contour(results)


def plot_results(results):
    epsilons = [res['epsilon'] for res in results]
    tvd_values = [res['tvd'] for res in results]
    upper_bounds = [res['upper_bound'] for res in results]

    plt.figure(figsize=(10, 6))
    plt.plot(epsilons, tvd_values, marker='o', label='TVD (measured)')
    plt.plot(epsilons, upper_bounds, marker='x', linestyle='--', label='Upper Bound (error_prob + leakage)')
    plt.xlabel('Epsilon')
    plt.ylabel('Value')
    plt.title('TVD vs Upper Bound comparison')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_error_probability_vs_epsilon(results):
    epsilons = [res['epsilon'] for res in results]
    error_probs = [res['error_prob'] for res in results]

    plt.figure(figsize=(8, 5))
    plt.plot(epsilons, error_probs, marker='o')
    plt.xlabel('Epsilon (ε)')
    plt.ylabel('Error Probability P(u ≠ û)')
    plt.title('Error Decoding Probability vs Epsilon')
    plt.grid(True)
    plt.show()

def plot_mutual_information_vs_delta(results):
    deltas = [res['delta'] for res in results]
    leakages = [res['leakage'] for res in results]

    plt.figure(figsize=(8, 5))
    plt.plot(deltas, leakages, marker='x')
    plt.xlabel('Delta (δ)')
    plt.ylabel('Mutual Information I(U;Z)')
    plt.title('Mutual Information vs Delta')
    plt.grid(True)
    plt.show()

def plot_security_contour(results):
    # Prepara i dati per il contour plot
    epsilons = sorted(list(set(res['epsilon'] for res in results)))
    deltas = sorted(list(set(res['delta'] for res in results)))

    epsilon_vals = []
    delta_vals = []
    tvd_vals = []

    for res in results:
        epsilon_vals.append(res['epsilon'])
        delta_vals.append(res['delta'])
        tvd_vals.append(res['tvd'])

    epsilon_vals = np.array(epsilon_vals)
    delta_vals = np.array(delta_vals)
    tvd_vals = np.array(tvd_vals)

    grid_x, grid_y = np.meshgrid(np.linspace(min(epsilons), max(epsilons), 100),
                                 np.linspace(min(deltas), max(deltas), 100))

    grid_z = griddata((epsilon_vals, delta_vals), tvd_vals, (grid_x, grid_y), method='cubic')

    plt.figure(figsize=(10, 7))
    contour = plt.contourf(grid_x, grid_y, grid_z, levels=20, cmap='viridis')
    plt.colorbar(contour, label='Security Level d(M, M*) (TVD)')
    plt.xlabel('Epsilon (ε)')
    plt.ylabel('Delta (δ)')
    plt.title('Security Level d(M, M*) Contour Plot')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
