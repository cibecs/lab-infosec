import numpy as np

import itertools
import matplotlib.pyplot as plt

#improves the printing of arrays
#np.set_printoptions(legacy='1.25')

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

def are_the_same_array_index(a, all_errors):
    for i in range(len(all_errors)):
        if len(a) != len(all_errors[i]):
            raise ValueError("Array length should be equal")
        for k in range(len(a)):
            if a[k].any() == all_errors[i][k].any():
                return i
    return -1

def validateIndependency(x, n_iterations, num_bits, max_errors_channel, max_errors_eavesdropper):
    all_channel_errors = generateAllErrors(num_bits, max_errors_channel)
    all_eavesdropper_errors = generateAllErrors(num_bits, max_errors_eavesdropper)
    all_channel_errors_with_xor = [xor_between_vectors(x, i) for i in all_channel_errors]
    all_eavesdropper_errors_with_xor = [xor_between_vectors(x, i) for i in all_eavesdropper_errors]

    errors_channel = {"".join(str(bit) for bit in i): 0 for i in all_channel_errors_with_xor}  # Initialize for all possible edit distances
    errors_eavesdropper = {"".join(str(bit) for bit in i): 0 for i in all_eavesdropper_errors_with_xor}  # Initialize for all possible edit distances

    for i in range(n_iterations):
        b = getRandomElement(all_channel_errors_with_xor)
        c = getRandomElement(all_eavesdropper_errors_with_xor)
        key = "".join(str(bit) for bit in b)
        errors_channel[key] += 1
        key = "".join(str(bit) for bit in c)
        errors_eavesdropper[key] += 1
    
    return errors_channel, errors_eavesdropper


#histogram errors for the channel and eavesdropper
def plot_statistic(title, errors):
    # Sort errors by count (optional but often useful)
    sorted_errors = dict(sorted(errors.items(), key=lambda item: item[1], reverse=True))

    plt.figure(figsize=(15, 4))
    bars = plt.bar(sorted_errors.keys(), sorted_errors.values(), color='#b3071b')  # solid blue

    # Add value labels above bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 4, height + 0.5,
                 f'{int(height)}', ha='center', va='bottom', fontsize=9)

    plt.xlabel('Error Pattern', fontsize=11)
    plt.ylabel('Count', fontsize=11)
    plt.title(title, fontsize=13, weight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(fontsize=9)
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()

def main():
    num_bits = 7  # Lunghezza del vettore
    errors_channel, errors_eavesdropper = validateIndependency(a, 100000, num_bits, 1, 3)
    plot_statistic("Channel", errors_channel)
    plot_statistic("Eavesdropper", errors_eavesdropper)

if __name__ == "__main__":
    main()


