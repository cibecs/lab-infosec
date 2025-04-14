import numpy as np

import itertools
import matplotlib as plt

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

def validateIndependency (x, iterations, num_bits, max_errors_channel, max_errors_eavesdropper):
    all_channel_errors = generateAllErrors(num_bits, max_errors_channel)
    all_eavesdropper_errors = generateAllErrors(num_bits, max_errors_eavesdropper)
    errors_channel = {}
    errors_eavesdropper = {}
    for i in range(max_errors_channel):
        errors_channel[i] = 0
    for i in range(max_errors_eavesdropper):
        errors_eavesdropper[i] = 0


    for i in range (iterations):
        b = getRandomElement(all_channel_errors)
        c = getRandomElement(all_eavesdropper_errors)
        y = xor_between_vectors(x, b)
        errors_channel[edit_distance_between_vectors(x, y)] +=1
        z = xor_between_vectors(x, c)
        errors_eavesdropper [edit_distance_between_vectors(x, z)] +=1
    
    return errors_channel, errors_eavesdropper

 

#histogram errors for the channel and eavesdropper
def plot_statistic(input_label, number_of_channels, errors):
    plt.bar(range(len(errors)), errors.values(), label="stats", color="red")
    plt.ylim(0, max(errors.values()) + 1)
    plt.xticks(range(len(errors)), errors.keys())
    plt.legend()
    plt.ylabel("Errors per word")
    plt.xlabel("Edit distance")
    plt.title(f"Graph for the Statistical Independencies: {input_label}")
    plt.grid()
    plt.show()

def main():
    validateIndependency(a, 10, 7 , 1, 3)
   

if __name__ == "__main__":
    main()    


    