from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# == Oracle setup ==
# In real CTFS, FLAG and KEY is not given
# Do not access FLAG and KEY variable
FLAG = b"NYRCS{ecb_is_very_insecure}"
KEY = os.urandom(16)  # Random AES-128 key

def encryption_oracle(user_input):
    plaintext = pad(user_input + FLAG, 16)
    cipher = AES.new(KEY, AES.MODE_ECB)
    return cipher.encrypt(plaintext)
# == End of oracle ==

# == Write code below ==

def byte_at_a_time(block_size):
    recovered = b""
    flag_length = len(encryption_oracle(b""))

    for _ in range(flag_length):
        padding_length = block_size - (len(recovered) % block_size) - 1
        padding = b"0" * padding_length
        block_index = len(recovered) // block_size

        cipher = encryption_oracle(padding)
        target = cipher[block_size*block_index : block_size*(block_index+1)]

        # Brute force to match target
        for b in range(256):
            # bytes([b]) : converts integer b into byte string
            brute_padding = padding + recovered + bytes([b])
            brute_cipher = encryption_oracle(brute_padding)
            brute_target = brute_cipher[block_size*block_index : block_size*(block_index+1)]

            if brute_target == target:
                recovered += bytes([b])
                break
    return recovered

recovered = byte_at_a_time(16)
print(f"flag={recovered.decode(errors='ignore')}")