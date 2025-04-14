def generate_random_keys(num_keys, dim=8, p=11):
    """Generate num_keys random keys of size (dim,)."""
    return [np.random.randint(0, p, size=dim) for _ in range(num_keys)]

def meet_in_the_middle_attack(plaintexts, ciphertexts, num_keys=10000):
    """Perform a meet-in-the-middle attack on the given plaintext-ciphertext pairs."""
    print("[*] Starting Meet-in-the-Middle Attack...")

    # Step 1: Generate N' random guesses for k'
    k_prime_candidates = generate_random_keys(num_keys, dim, p)
    forward_table = {}

    for k_prime in k_prime_candidates:
        intermediate_values = [encryption(u, k_prime) for u in plaintexts]
        for inter_val in intermediate_values:
            forward_table[tuple(inter_val)] = k_prime  # Store (intermediate_state -> key)

    print(f"[*] Forward table generated with {len(forward_table)} entries.")

    # Step 2: Generate N'' random guesses for k''
    k_double_prime_candidates = generate_random_keys(num_keys, dim, p)
    backward_table = {}

    for k_double_prime in k_double_prime_candidates:
        decrypted_values = [encryption(x, k_double_prime) for x in ciphertexts]
        for dec_val in decrypted_values:
            backward_table[tuple(dec_val)] = k_double_prime  # Store (intermediate_state -> key)

    print(f"[*] Backward table generated with {len(backward_table)} entries.")

    # Step 3: Find matches in the tables
    for intermediate_state in forward_table.keys():
        if intermediate_state in backward_table:
            k_prime_guess = forward_table[intermediate_state]
            k_double_prime_guess = backward_table[intermediate_state]
            print(f"[+] Found matching keys: k' = {k_prime_guess}, k'' = {k_double_prime_guess}")
            return k_prime_guess, k_double_prime_guess

    print("No matching keys found")
    return None, None

# Read known plaintext-ciphertext pairs
filepath = "KPAdataH_CyberDucks/KPAdataH/KPApairsH_nearly_linear.txt"
plaintexts, ciphertexts = read_pairs_from_file(filepath)

# Run the Meet-in-the-Middle attack
k_prime, k_double_prime = meet_in_the_middle_attack(plaintexts, ciphertexts)
print(k_prime)
print(k_double_prime)