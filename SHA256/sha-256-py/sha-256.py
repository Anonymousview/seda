import struct

# Constant initialization
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

# Initial hash values
H = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
]

def right_shift(value: int, shift: int, bit_length: int = 32):
    return (value >> shift)

def right_rotate(value: int, shift: int, bit_length: int = 32):
    return (value >> shift) | (value << (bit_length - shift)) & 0xFFFFFFFF

def sigma0(x: int):
    return right_rotate(x, 7) ^ right_rotate(x, 18) ^ right_shift(x, 3)

def sigma1(x: int):
    return right_rotate(x, 17) ^ right_rotate(x, 19) ^ right_shift(x, 10)

def SIGMA0(x: int):
    return right_rotate(x, 2) ^ right_rotate(x, 13) ^ right_rotate(x, 22)

def SIGMA1(x: int):
    return right_rotate(x, 6) ^ right_rotate(x, 11) ^ right_rotate(x, 25)

def Ch(x: int, y: int, z: int):
    return (x & y) ^ (~x & z)

def Maj(x: int, y: int, z: int):
    return (x & y) ^ (x & z) ^ (y & z)

def sha256(message: bytes):
    # Convert the message to a mutable bytearray
    message = bytearray(message)

    if isinstance(message, str):
        message = bytearray(message, 'ascii')
    elif isinstance(message, bytes):
        message = bytearray(message)
    elif not isinstance(message, bytearray):
        raise TypeError
    
    # Padding the message
    original_byte_len = len(message)
    original_bit_len = original_byte_len * 8
    message.append(0x80)  # Append a 1
    while (len(message) * 8 + 64) % 512 != 0:
        message.append(0x00) 
    
    message += original_bit_len.to_bytes(8, 'big') # Pad to 8 bytes or 64 bits

    assert (len(message) * 8) % 512 == 0, "Padding error!"

    # Process each 512-bit block
    for i in range(0, len(message), 64):
        w = list(struct.unpack('>16L', message[i:i + 64])) # Unpack a 64-byte block of the message into 16 32-bit unsigned integers and store them in list w
        for j in range(16, 64): # Generate (64-16) 32-bit unsigned integers
            s0 = sigma0(w[j - 15])
            s1 = sigma1(w[j - 2])
            w.append((w[j - 16] + s0 + w[j - 7] + s1) & 0xFFFFFFFF)

        # Set initial hash values
        a, b, c, d, e, f, g, h = H

        for j in range(64): # 64 rounds of processing
            S0 = (SIGMA1(e) + Ch(e, f, g) + h + K[j] + w[j]) & 0xFFFFFFFF
            S1 = (SIGMA0(a) + Maj(a, b, c)) & 0xFFFFFFFF

            h = g
            g = f
            f = e
            e = (d + S0) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (S1 + S0) & 0xFFFFFFFF

        # Compute intermediate hash values
        H[0] = (H[0] + a) & 0xFFFFFFFF
        H[1] = (H[1] + b) & 0xFFFFFFFF
        H[2] = (H[2] + c) & 0xFFFFFFFF
        H[3] = (H[3] + d) & 0xFFFFFFFF
        H[4] = (H[4] + e) & 0xFFFFFFFF
        H[5] = (H[5] + f) & 0xFFFFFFFF
        H[6] = (H[6] + g) & 0xFFFFFFFF
        H[7] = (H[7] + h) & 0xFFFFFFFF

    return ''.join(f'{x:08x}' for x in H)


if __name__ == '__main__':
    message = "Hello, World!"
    hash_value = sha256(message.encode('utf-8'))
    print(f"[Python] SHA-256 of '{message}': {hash_value}")
