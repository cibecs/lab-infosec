import numpy as np
from task1 import n, p, multiplicative_value_of_f, A,k,  test, subkey_generation

x = np.array([4, 0, 0, 9, 7, 0, 0, 3])

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

def decryption(x, n):
    subkey = subkey_generation(k)
    w = inverse_subkey_sum(x, subkey[n])  # Annulla l'ultima somma
    for i in range(n - 1, -1, -1):  # Decifra nei round inversi
        z = inverse_linear(w) if i != n - 1 else w
        y = inverse_transposition(z)
        v = inverse_substitution(y)
        w = inverse_subkey_sum(v, subkey[i])
    return w.copy()

def main ():
    u = decryption(x, n)
    u_test = [1, 0, 0, 0, 0, 0, 0, 0]
    test(u, u_test)

if __name__ == "__main__": 
    main()