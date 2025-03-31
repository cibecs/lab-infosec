import numpy as np
n = 5 #number of rounds
p = 11

u = [1,0,0,0,0,0,0,0]
k = [1,0,0,0,0,0,0,0]

def subkey_generation(k):
    k1 = [k[0], k[2], k[4], k[6]]
    k2 = [k[0], k[1], k[2], k[3]]
    k3 = [k[0], k[3], k[4], k[7]] 
    k4 = [k[0], k[3], k[5], k[6]]
    k5 = [k[0], k[2], k[5], k[7]]
    k6 = [k[2], k[3], k[4], k[5]]
    return [k1, k2, k3, k4, k5, k6]

def subkey_sum(wi_1, ki):
    k = ki + ki
    v = []
    for i in range(0, len(k)):
        v.append((wi_1[i % len(wi_1)] + k[i]) % p)
    return v

def substitution(v):
    y = []
    for i in range(0, len(v)):
        y.append(2*v[i] % p)
    return y

def transposition(y):
    #da fare meglio con numpy
    z = np.array(y)[[0, 1, 2, 3, 7, 6, 5, 4]]
    return z

def linear(z):
    A = np.array([[2, 5], [1, 7]])
    w = z.reshape(2, 4)
    w = np.dot(A, w) % p
    return w.flatten()

subkey = subkey_generation(k)

w = u.copy()
for i in range(0, n):
    v = subkey_sum(w, subkey[i])
    y = substitution(v)
    z = transposition(y)
    if i != n-1: w = linear(z)
x = subkey_sum(z, subkey[n])
print(x)

#check
x_test = [4, 0, 0, 9, 7, 0, 0, 3]
if x == x_test:
    print("Test passed")
else:
    print("Test failed")