import numpy as np
from task1 import p, n, multiplicative_value_of_f, subkey_sum, transposition, linear

u = np.array([1, 0, 0, 0, 0, 0, 0, 0])
k = np.array([1, 0, 0, 0])

def subkey_generation(k):
    k1 = [k[0], k[1], k[2], k[3]]
    k2 = [k[0], k[1], k[3], k[2]]
    k3 = [k[1], k[2], k[3], k[0]] 
    k4 = [k[0], k[3], k[1], k[2]]
    k5 = [k[2], k[3], k[0], k[1]]
    k6 = [k[1], k[3], k[0], k[2]]
    return np.array([
        k1, k2, k3, k4, k5, k6
    ])

def modular_inverse(v):
    """Calcola l'inverso moltiplicativo modulo p per ogni elemento di v"""
    inverses = []
    for x in v:
        #nel nostro caso p = 11, l'unico numero non invertibile è 0
        if np.gcd(x, p) == 1:
            inverses.append(pow(int(x), -1, p))
        else:
            inverses.append(0)
    return np.array(inverses)

def substitution(v):
    v_inv = modular_inverse(v)  # Calcola l'inverso modulo p
    return (multiplicative_value_of_f * v_inv) % p  # Applica la substitution

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
    x_test = [5, 0, 3, 2, 5, 2, 1, 1]
    x = encryption(u, k)
    test(x, x_test)

if __name__ == "__main__":
    main()