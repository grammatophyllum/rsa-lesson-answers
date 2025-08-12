from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

BLOCK_SIZE = 16

key = get_random_bytes(16)
iv = get_random_bytes(16)
plaintext = b"this is a long plaintext that spans multiple blocks!!!"
cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = iv + cipher.encrypt(pad(plaintext, BLOCK_SIZE))

def padding_oracle(test_ciphertext: bytes) -> bool:
    cipher = AES.new(key, AES.MODE_CBC, test_ciphertext[:BLOCK_SIZE])
    try:
        unpad(cipher.decrypt(test_ciphertext[BLOCK_SIZE:]), BLOCK_SIZE)
        return True
    except ValueError:
        return False

def split_blocks(data: bytes):
    return [data[i:i+BLOCK_SIZE] for i in range(0, len(data), BLOCK_SIZE)]

def recover_block(prev_block: bytes, target_block: bytes):
    prev = bytearray(prev_block)
    intermediate = [None] * BLOCK_SIZE
    recovered = [None] * BLOCK_SIZE

    # recursive backtracking, pos from 15 (last byte) down to 0
    def recover_at(pos: int) -> bool:
        pad_val = BLOCK_SIZE - pos

        # prepare the prefix base (we'll copy it for each guess)
        base = bytearray(prev_block)

        # set bytes after pos to enforce padding=pad_val using known intermediate values
        for j in range(1, pad_val):
            iv_index = -j
            base[iv_index] = intermediate[iv_index] ^ pad_val # type: ignore

        # gather all candidate guesses that produce "valid padding"
        candidates = []
        for guess in range(256):
            test = bytearray(base)
            test[-pad_val] = guess
            if padding_oracle(bytes(test) + target_block):
                candidates.append(guess)

        # try each candidate and recurse (backtracking)
        for g in candidates:
            inter_val = g ^ pad_val
            intermediate[-pad_val] = inter_val
            recovered[-pad_val] = inter_val ^ prev[-pad_val]

            # if we've recovered the whole block or can recover earlier bytes, succeed
            if pos == 0 or recover_at(pos - 1):
                # debug print (optional)
                ch = recovered[-pad_val]
                printable = chr(ch) if 32 <= ch < 127 else f"0x{ch:02x}" # type: ignore
                print(f"[pad={pad_val:02}] byte={pos:02} guess=0x{g:02x} -> {printable}")
                return True

            # backtrack
            intermediate[-pad_val] = None
            recovered[-pad_val] = None

        return False

    ok = recover_at(BLOCK_SIZE - 1)
    if not ok:
        raise RuntimeError("Failed to recover block (backtracking exhausted).")
    return bytes(recovered) # type: ignore

# recover all blocks (skip the IV block at index 0)
blocks = split_blocks(ciphertext)
full = b""
for i in range(1, len(blocks)):
    print(f"\nRecovering plaintext block {i-1} (from C{i}):")
    b_plain = recover_block(blocks[i-1], blocks[i])
    full += b_plain

print("Recovered:", unpad(full, BLOCK_SIZE))
