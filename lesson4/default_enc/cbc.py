from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

BLOCK_SIZE = 16
key = os.urandom(16)

def encrypt_cbc(plaintext, key):
    iv = os.urandom(BLOCK_SIZE) # Optional
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, BLOCK_SIZE))
    return iv + ciphertext

def decrypt_cbc(ciphertext, key):
    iv = ciphertext[:BLOCK_SIZE]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext[BLOCK_SIZE:]), BLOCK_SIZE)
    return plaintext

pt = b"cbc_is_safer"
enc = encrypt_cbc(pt, key)
dec = decrypt_cbc(enc, key)

print(f"Plaintext: {pt}")
print(f"Ciphertext (hex): {enc.hex()}")
print(f"Decrypted: {dec}")