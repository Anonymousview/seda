class CTR:
    def __init__(self, cipher, nonce):
        self.cipher = cipher
        self.nonce = nonce

    def _xor(self, data_1, data_2):
        return bytes([a ^ b for a, b in zip(data_1, data_2)])

    def _get_iv(self, counter):
        # Combine nonce and counter to make IV
        # len(nonce + counter) should be equal to the block size: 16 bytes (128 bits) for AES
        # len(nonce) == 10 bytes by definition
        # len(counter) == 6 bytes by definition
        counter_bytes = counter.to_bytes(6, byteorder="big")
        return self.nonce + counter_bytes
    
    def encrypt(self, data_block, counter):
        IV = self._get_iv(counter)
        ciphertext = self._xor(self.cipher.encrypt(IV), data_block)
        return ciphertext

    def decrypt(self, cipher_block, counter):
        # Decryption is the same as encryption
        return self.encrypt(cipher_block, counter)
