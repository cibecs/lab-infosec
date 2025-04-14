import numpy as np

def generate_key(pisnelo: str, length: int, p: int):
    # Convert the input string into ASCII values
    ascii_values = [ord(char) for char in pisnelo]
    
    # Convert to values modulo p
    mod_values = [val % p for val in ascii_values]
    
    # Repeat or truncate the sequence to match the desired length
    key_vector = (mod_values * ((length // len(mod_values)) + 1))[:length]
    
    return np.array(key_vector)

# Example usage
pisnelo = 'pisnelo'
length = 8
p = 11
key = generate_key(pisnelo, length, p)
print(key)

