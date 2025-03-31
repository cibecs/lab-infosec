import numpy as np
n = 5 #number of rounds
p = 11
multiplicative_value_of_f = 2
A = np.array([[2, 5], [1, 7]])

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
    k = np.tile(ki, 2)  # k = ki + ki
    return (w + k[:len(w)]) % p

def substitution(v):
    return (multiplicative_value_of_f * v) % p

def transposition(y):
    # flipped the second half of vector yi
    return np.array(y)[[0, 1, 2, 3, 7, 6, 5, 4]]


def linear(z):
    # linear transformation: write (by rows) vector zi to 2 × 4 matrix Z
    w = z.reshape(2, 4)
    w = (A @ w) % p
    return w.flatten()

subkey = subkey_generation(k)

w = u.copy()
for i in range(n):
    v = subkey_sum(w, subkey[i])
    y = substitution(v)
    z = transposition(y)
    if i != n-1: w = linear(z)
x = subkey_sum(z, subkey[n])
print(x)

#check
x_test = [4, 0, 0, 9, 7, 0, 0, 3]
if np.array_equal(x, x_test):
    print("Test passed")
else:
    print("Test failed")