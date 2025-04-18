from task1 import n, k, u, test, subkey_generation, subkey_sum, transposition, linear, encryption

substitution_map = {0: 0, 1: 2, 2: 4, 3: 8, 4: 6, 5: 10, 6: 1, 7: 3, 8: 5, 9: 7, 10: 9}

def substitution(v):
    # substitution: apply substitution map to vector v
    for i in range(len(v)):
        v[i] = substitution_map[v[i]]
    return v

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

def main():
    u = [0,0,0,0,0,0,0,0]
    k = [1,0,0,0,0,0,0,0]
    x = encryption(u, k)
    x_test = [2,7,6,8,1,7,9,3]
    test(x, x_test)

if __name__ == "__main__":
    main()
    