import numpy as np
from task2 import encoder_plus_channel_errors
from task1 import plot_statistic

import itertools

all_possible_input = [list(tupla) for tupla in itertools.product([0, 1], repeat=3)]

def empirical_distribution_of_z(all_possible_input, iterations):
    for u in all_possible_input:
        all_possible_codewords_with_channel_errors  = {
                                                   "".join(str(bit) for bit in i): 0 for i 
                                                   in [list(tupla) for tupla in itertools.product([0, 1], repeat=7)]
                                                   }
        for _ in range(iterations):
            t = encoder_plus_channel_errors(u, True)
            key = "".join(str(bit) for bit in t)
            all_possible_codewords_with_channel_errors[key] += 1
        
        plot_statistic(f"Empirical distribution of {u}", all_possible_codewords_with_channel_errors)

def main():
    empirical_distribution_of_z(all_possible_input, 10000)

if __name__ == "__main__":
    main()