import numpy as np
n = 5 #number of rounds
p = 11
multiplicative_value_of_f = 2
A = np.array([[2, 5], [1, 7]])

x = np.array([4, 0, 0, 9, 7, 0, 0, 3])
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

def inverse_subkey_sum(w, ki):
    k = np.tile(ki, 2)  # k = ki + ki
    return (w - k[:len(w)] + p) % p # I add p to avoid negative values

def inverse_substitution(v):
    inverse_of_multiplicative_value_of_f = pow(multiplicative_value_of_f, -1, p)
    return (v * inverse_of_multiplicative_value_of_f) % p

def inverse_transposition(y):
    return np.array(y)[[0, 1, 2, 3, 7, 6, 5, 4]]

def modular_inverse_matrix(A, p):
    det = int(np.round(np.linalg.det(A))) % p  # Determinante modulo p
    det_inv = pow(det, -1, p)  # Inverso del determinante mod p
    A_inv = np.round(det_inv * np.linalg.inv(A) * det) % p  # Matrice inversa mod p
    return A_inv.astype(int)  # Converti in interi

def inverse_linear(z):
    A_inv = modular_inverse_matrix(A, p)
    w = z.reshape(2, 4)
    w = (A_inv @ w) % p
    return w.flatten()

subkey = subkey_generation(k)

def decryption(x, subkey, n):
    w = inverse_subkey_sum(x, subkey[n])  # Annulla l'ultima somma
    for i in range(n - 1, -1, -1):  # Decifra nei round inversi
        z = inverse_linear(w) if i != n - 1 else w
        y = inverse_transposition(z)
        v = inverse_substitution(y)
        w = inverse_subkey_sum(v, subkey[i])
    return w.copy()

u = decryption(x, subkey, n)
print(u)

def test(result, target):
    if np.array_equal(result, target):
        print("Test passed")
    else:
        print("Test failed")

u_test = [1, 0, 0, 0, 0, 0, 0, 0]
test(u, u_test)