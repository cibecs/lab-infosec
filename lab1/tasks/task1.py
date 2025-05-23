import numpy as np
n = 5 #number of rounds
p = 11
multiplicative_value_of_f = 2
matrix_A = np.array([[2, 5], [1, 7]])

u = np.array([1, 0, 0, 0, 0, 0, 0, 0])
k = np.array([1, 0, 0, 0, 0, 0, 0, 0])

def subkey_generation(k):
    k1 = [k[0], k[2], k[4], k[6]]
    k2 = [k[0], k[1], k[2], k[3]]
    k3 = [k[0], k[3], k[4], k[7]] 
    k4 = [k[0], k[3], k[5], k[6]]
    k5 = [k[0], k[2], k[5], k[7]]
    k6 = [k[2], k[3], k[4], k[5]]
    return np.array([
        k1, k2, k3, k4, k5, k6
    ])

def subkey_sum(w, ki):
    subkey = np.tile(ki, 2)  # k = ki + ki
    return (w + subkey[:len(w)]) % p

def substitution(v):
    return (multiplicative_value_of_f * v) % p

def transposition(y):
    # flipped the second half of vector yi
    return np.array(y)[[0, 1, 2, 3, 7, 6, 5, 4]]


def linear(z):
    # linear transformation: write (by rows) vector z to 2 × 4 matrix Z
    Z = z.reshape(2, 4)
    w = (matrix_A @ Z) % p
    return w.flatten()


def encryption(u, k):
    subkey = subkey_generation(k)
    w = u.copy()
    for i in range(n):
        v = subkey_sum(w, subkey[i])
        y = substitution(v)
        z = transposition(y)
        if i != n-1: 
            w = linear(z)
    x = subkey_sum(z, subkey[n])
    return x


def test(result, target):
    print(result)
    if np.array_equal(result, target):
        print("Test passed")
    else:
        print("Test failed")
def main():
    x_test = [4, 0, 0, 9, 7, 0, 0, 3]
    x = encryption(u, k)
    test(x, x_test)

if __name__ == "__main__":
    main()