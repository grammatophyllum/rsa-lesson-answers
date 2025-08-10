from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# Generate AES Key
KEY = os.urandom(16)  # Key is 16 bytes

# AES-ECB Encryption
def encrypt_ecb(plaintext):
    cipher = AES.new(KEY, AES.MODE_ECB)
    padded = pad(plaintext, 16)
    return cipher.encrypt(padded)

# AES-ECB Decryption
def decrypt_ecb(ciphertext):
    cipher = AES.new(KEY, AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    return unpad(decrypted, 16)

# b"" turns string into bytes
message = b"dancing capybaradancing capybaradancing capybara" 
print(f"Original: {message}")

ct = encrypt_ecb(message)
print(f"Ciphertext (hex): {ct.hex()}")

pt = decrypt_ecb(ct)
print(f"Decrypted: {pt}")
