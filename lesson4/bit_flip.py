from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# == SETUP ==
BLOCK_SIZE = 16
key = os.urandom(16)

def encrypt_cbc(plaintext, key):
    iv = b"\x00" * 16
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, BLOCK_SIZE))
    return ciphertext

def decrypt_cbc(ciphertext, key):
    iv = b"\x00" * 16
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)
    return plaintext

# Do not access plaintext
# Only access ciphertext
plaintext = b"text=helloworld?user=guest"
ciphertext = encrypt_cbc(plaintext, key)
print(f'c={ciphertext.hex()}')
# == END of SETUP ==

# == Write code below ==

def bit_flip(ciphertext, original_plaintext, target_plaintext, block_index=0, offset=0):
    blocks = [bytearray(ciphertext[i:i+16]) for i in range(0, len(ciphertext), 16)]
    for i in range(len(target_plaintext)):
        blocks[block_index][offset + i] ^= original_plaintext[i] ^ target_plaintext[i]
    return b''.join(blocks)

modified_ciphertext = bit_flip(
    ciphertext,
    original_plaintext=b"user=guest",
    target_plaintext=b"user=admin",
    block_index=0,
    offset=0  
)
print(f'new_c={modified_ciphertext.hex()}')

# Check if we have modified user=guest to user=admin
new_plaintext = decrypt_cbc(modified_ciphertext, key)
print(new_plaintext)

