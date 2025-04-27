import numpy as np
from collections import Counter
from task3 import decoder
from task2 import encoder


#PAM Modulator
def pam_modulate(bits, M=128):
    k = int(np.log2(M))  # number of bits per symbol
    if len(bits) % k != 0:
        raise ValueError(f"Il numero di bit deve essere multiplo di {k} per PAM-{M}")

    bits = np.array(bits)
    symbols = []

    for i in range(0, len(bits), k):
        group = bits[i:i+k]
        # Converte il gruppo di bit in un numero decimale
        decimal_value = 0
        for j in range(k):
            decimal_value += group[j] << (k - j - 1)

        # Map su simboli PAM: da 0..127 a livelli centrati attorno a 0
        pam_symbol = 2 * decimal_value - (M - 1)
        symbols.append(pam_symbol)

    return np.array(symbols)


def awgn_channel(signal, snr_db=10):
    # Calcola la potenza del segnale
    signal_power = np.mean(signal**2)

    # Calcola il rapporto segnale/rumore lineare (non in dB)
    snr_linear = 10**(snr_db / 10)

    # Calcola la potenza del rumore
    noise_power = signal_power / snr_linear

    # Genera il rumore bianco gaussiano
    noise = np.sqrt(noise_power) * np.random.randn(*signal.shape)

    # Segnale ricevuto = segnale originale + rumore
    received_signal = signal + noise

    return received_signal

def pam_demodulate(received_signal, M=128):
    k = int(np.log2(M))  # numero di bit per simbolo
    bits_out = []

    # Costruisci la mappa dei simboli PAM ideali
    pam_levels = np.arange(-(M-1), M, step=2)  # ad esempio, -127, -125, ..., 125, 127

    for y in received_signal:
        # Trova il simbolo PAM ideale più vicino
        idx = np.argmin(np.abs(pam_levels - y))
        symbol = idx  # simbolo corrispondente a valore decimale

        # Converte il simbolo in bit
        bits = [(symbol >> (k-1-j)) & 1 for j in range(k)]
        bits_out.extend(bits)

    return np.array(bits_out)

def encoder_plus_pam_and_awgn(input, snr_db=10):
    encoded_bits = []
    for i in range(0, len(input_bits), 3):
        group = input_bits[i:i+3]
        encoded = encoder(group)
        encoded_bits.extend(encoded)
    encoded_bits = np.array(encoded_bits)

    pam_symbols = pam_modulate(encoded_bits, M=128)
    return awgn_channel(pam_symbols, snr_db=snr_db)


def main():
    # Genera dei dati di input casuali
    input_bits = np.random.randint(0, 2, 300)  # 100 gruppi da 3 bit

    # Esegui tutta la catena con ad esempio 10 dB di SNR
    reconstructed_bits = full_chain(input_bits, snr_db=10)

    # Calcola e stampa il Bit Error Rate (BER)
    n_errors = np.sum(input_bits != reconstructed_bits)
    ber = n_errors / len(input_bits)
    print(f"Bit Error Rate (BER): {ber}")




if __name__ == "__main__":
    main()