import numpy as np
import itertools
import math
from collections import Counter, defaultdict
from task2 import generate_codewords
from task1 import MAX_ERRORS_EAVESDROPPER, xor_between_vectors, NUM_BITS, generateAllErrors, getRandomElement

# Tutti i possibili input u ∈ {0,1}^3
all_possible_input = [tuple(t) for t in itertools.product([0, 1], repeat=3)]
all_possible_z = ["".join(str(bit) for bit in i) for i in itertools.product([0, 1], repeat=7)]

def encoder_plus_eavesdropper(u):
    codeword = getRandomElement(generate_codewords(u))
    if codeword is None:
        raise ValueError("No valid codeword found for the given input.")
    error = getRandomElement(generateAllErrors(NUM_BITS, MAX_ERRORS_EAVESDROPPER))
    return "".join(str(bit) for bit in xor_between_vectors(codeword, error))

def empirical_joint_distribution(num_samples):
    joint_counts = Counter()
    total_samples = 0

    for u in all_possible_input:
        for _ in range(num_samples):
            z = encoder_plus_eavesdropper(u)
            joint_counts[(u, z)] += 1
            total_samples += 1

    return joint_counts, total_samples

def compute_distributions(joint_counts, total_samples):
    # Joint p(u,z)
    p_uz = {k: v / total_samples for k, v in joint_counts.items()}

    # Marginals
    p_u = defaultdict(float)
    p_z = defaultdict(float)
    for (u, z), p in p_uz.items():
        p_u[u] += p
        p_z[z] += p

    # Conditional p(z|u)
    p_z_given_u = dict()
    for (u, z), p_joint in p_uz.items():
        p_z_given_u[(z, u)] = p_joint / p_u[u] if p_u[u] > 0 else 0.0

    return p_uz, p_u, p_z, p_z_given_u

def compute_mutual_information(p_uz, p_u, p_z):
    I = 0.0
    for (u, z), p_joint in p_uz.items():
        if p_joint > 0:
            I += p_joint * math.log2(p_joint / (p_u[u] * p_z[z]))
    return I

def main():
    joint_counts, total_samples = empirical_joint_distribution(num_samples=100000)

    p_uz, p_u, p_z, p_z_given_u = compute_distributions(joint_counts, total_samples)

    I_u_z = compute_mutual_information(p_uz, p_u, p_z)

    print(f"\nEstimated Mutual Information I(u; z): {I_u_z:.6f}")

if __name__ == "__main__":
    main()
