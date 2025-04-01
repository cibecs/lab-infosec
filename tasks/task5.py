import numpy as np
n = 5 #number of rounds
p = 11
multiplicative_value_of_f = 2
A = np.array([[2, 5], [1, 7]])

u = np.array([1, 0, 0, 0, 0, 0, 0, 0])
k = np.array([1, 0, 0, 0, 0, 0, 0, 0])

substitution_map = {
    0: 0,
    1: 2, 
    2: 4,
    3: 8, 
    4: 6, 
    5: 10, 
    6: 1, 
    7: 3,
    8: 5,
    9: 7,
    10: 9
}

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
    k = np.tile(ki, 2)  # k = ki + ki
    return (w + k[:len(w)]) % p

def substitution(v):
    # substitution: apply substitution map to vector v
    for i in range(len(v)):
        v[i] = substitution_map[v[i]]
    return v

def transposition(y):
    # flipped the second half of vector yi
    return np.array(y)[[0, 1, 2, 3, 7, 6, 5, 4]]


def linear(z):
    # linear transformation: write (by rows) vector z to 2 × 4 matrix Z
    Z = z.reshape(2, 4)
    w = (A @ Z) % p
    return w.flatten()

subkey = subkey_generation(k)

def encryption(u, n, subkey, p):
    w = u.copy()
    for i in range(n):
        v = subkey_sum(w, subkey[i])
        y = substitution(v)
        z = transposition(y)
        if i != n-1: 
            w = linear(z)
    x = subkey_sum(z, subkey[n])
    return x

x = encryption(u, n, subkey, p)
print(x)


x_test = [9, 0, 0, 0, 5, 0, 0, 6]
def test(result, target):
    if np.array_equal(result, target):
        print("Test passed")
    else:
        print("Test failed")

test(x, x_test)