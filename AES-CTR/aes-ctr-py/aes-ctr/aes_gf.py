# This is an implementation of AES in Python
# Supports AES-128, AES-192, AES-256

import numpy as np
import hashlib


class AES:
    def __init__(self, key, key_len=256):
        # AES block size is 16 bytes (128 bits)
        self.block_size = 16
        # self.salt = salt
        self.key_len = key_len
        # self.key = key.encode("UTF-8")
        # self.key = key
        self.key = np.frombuffer(key, dtype=np.uint8).reshape((self.key_len // 8 // 4, 4))

        # AES number of rounds (key_len, rounds): (128, 10), (192,12), (256, 14)
        self.rounds = self.key_len // 32 + 6

        # Key expansion
        self.keys = self.KeyExpansion(key=self.key, rounds=self.rounds)

    #### Real-time generate Sbox in GF(2^8)
    @staticmethod
    def bit_transform_mapping(q):
        q7, q6, q5, q4, q3, q2, q1, q0 = q
        k7 = q7 ^ q5
        k6 = q7 ^ q6 ^ q4 ^ q3 ^ q2 ^ q1
        k5 = q7 ^ q5 ^ q3 ^ q2
        k4 = q7 ^ q5 ^ q3 ^ q2 ^ q1
        k3 = q7 ^ q6 ^ q2 ^ q1
        k2 = q7 ^ q4 ^ q3 ^ q2 ^ q1
        k1 = q6 ^ q4 ^ q1
        k0 = q6 ^ q1 ^ q0
        return [k7, k6, k5, k4, k3, k2, k1, k0]

    @staticmethod
    def bit_transform_gf24_XX(q):
        q3, q2, q1, q0 = q
        k3 = q3
        k2 = q3 ^ q2
        k1 = q2 ^ q1
        k0 = q3 ^ q1 ^ q0
        return [k3, k2, k1, k0]

    @staticmethod
    def bit_transform_gf24_XC(q):
        q3, q2, q1, q0 = q
        k3 = q2 ^ q0
        k2 = q3 ^ q2 ^ q1 ^ q0
        k1 = q3
        k0 = q2
        return [k3, k2, k1, k0]


    @staticmethod
    def bit_transform_gf22_XY(q, w):
        q1, q0 = q
        w1, w0 = w
        k1 = (q1 * w1) ^ (q0 * w1) ^ (q1 * w0)
        k0 = (q1 * w1) ^ (q0 * w0)
        return [k1, k0]

    @staticmethod
    def bit_transform_gf22_XC(q):
        q1, q0 = q
        k1 = q1 ^ q0
        k0 = q1
        return [k1, k0]

    from itertools import product
    @staticmethod
    def bitwise_xor(qn, wn, n):
        if len(qn) != n or len(wn) != n:
            raise ValueError("The length of the input variable must be equal to n")
        
        result = [qn[i] ^ wn[i] for i in range(n)]
        return result

    @staticmethod
    def bit_transform_gf24_XY(q, w):
        q3, q2, q1, q0 = q
        qh = [q3, q2]
        ql = [q1, q0]

        w3, w2, w1, w0 = w
        wh = [w3, w2]
        wl = [w1, w0]

        [k3, k2] = AES.bitwise_xor(AES.bitwise_xor(AES.bit_transform_gf22_XY(qh, wh), AES.bit_transform_gf22_XY(qh, wl), 2), AES.bit_transform_gf22_XY(ql, wh), 2)
        [k1, k0] = AES.bitwise_xor(AES.bit_transform_gf22_XC(AES.bit_transform_gf22_XY(qh, wh)), AES.bit_transform_gf22_XY(ql, wl),2)
        return [k3, k2, k1, k0]

    @staticmethod
    def bit_transform_gf24_mul_inv(q):
        q3, q2, q1, q0 = q
        
        k3 = q3 ^ (q3 & q2 & q1) ^ (q3 & q0) ^ q2
        k2 = (q3 & q2 & q1) ^ (q3 & q2 & q0) ^ (q3 & q0) ^ q2 ^ (q2 & q1)
        k1 = q3 ^ (q3 & q2 & q1) ^ (q3 & q1 & q0) ^ q2 ^ (q2 & q0) ^ q1
        k0 = (q3 & q2 & q1) ^ (q3 & q2 & q0) ^ (q3 & q1) ^ (q3 & q1 & q0) ^ (q3 & q0) ^ q2 ^ (q2 & q1) ^ (q2 & q1 & q0) ^ q1 ^ q0
        
        return [k3, k2, k1, k0]

    @staticmethod
    def bit_transform_gf28_mul_inv_affine(q):
        q7, q6, q5, q4, q3, q2, q1, q0 = q
        k7 = q7 ^ q3 ^ q2
        k6 = q7 ^ q6 ^ q5 ^ q4 ^ 1
        k5 = q7 ^ q2 ^ 1
        k4 = q7 ^ q4 ^ q1 ^ q0
        k3 = q2 ^ q1 ^ q0
        k2 = q6 ^ q5 ^ q4 ^ q3 ^ q2 ^ q0
        k1 = q7 ^ q0 ^ 1
        k0 = q7 ^ q6 ^ q2 ^ q1 ^ q0 ^ 1
        return [k7, k6, k5, k4, k3, k2, k1, k0]

    def bit_transform_gf28(q):
        if all(bit == 0 for bit in q):
            k = [0, 1, 1, 0, 0, 0, 1, 1]
        else:
            q7, q6, q5, q4, q3, q2, q1, q0 = q
            qh = [q7, q6, q5, q4]
            ql = [q3, q2, q1, q0]

            # isomorphic mapping to composite fields
            [q7_map, q6_map, q5_map, q4_map, q3_map, q2_map, q1_map, q0_map] = AES.bit_transform_mapping(q)
            qh_map = [q7_map, q6_map, q5_map, q4_map]
            ql_map = [q3_map, q2_map, q1_map, q0_map]

            # squarer in GF(2^4)
            qh_map_xx = AES.bit_transform_gf24_XX(qh_map)
            # multiplication with constant in GF(2^4)
            qh_map_xx_xc = AES.bit_transform_gf24_XC(qh_map_xx)

            xor_qh_ql = AES.bitwise_xor(qh_map, ql_map, 4)
            # multiplication operation in GF(2^4)
            xor_qh_ql_xy = AES.bit_transform_gf24_XY(xor_qh_ql, ql_map)

            state = AES.bitwise_xor(qh_map_xx_xc, xor_qh_ql_xy, 4)
            # multiplication inversion in GF(2^4)
            state_inv = AES.bit_transform_gf24_mul_inv(state)

            [k7, k6, k5, k4] = AES.bit_transform_gf24_XY(state_inv, qh_map)
            [k3, k2, k1, k0] = AES.bit_transform_gf24_XY(state_inv, xor_qh_ql)

            # inverse isomorphic mapping to GF(2^8) + affine transformation
            k = AES.bit_transform_gf28_mul_inv_affine([k7, k6, k5, k4, k3, k2, k1, k0])

        # Convert the list to a binary string
        binary_str = ''.join(map(str, k))
        # Convert the binary string to a uint8 decimal number
        decimal_k = np.uint8(int(binary_str, 2) & 0xFF)
        # Convert the uint8 decimal number to an 8-bit byte
        byte_k = decimal_k.tobytes()
        return byte_k
    
        #  # Convert the list to a binary string
        # binary_str = ''.join(map(str, k))
        # # Convert the binary string to a uint8 decimal number
        # decimal_k = np.uint8(int(binary_str, 2) & 0xFF)
        # return decimal_k


    def KeyExpansion(self, key, rounds):
        # Generating rcon by doubling rcon's previous value in GF(2^8)
        # Only need 10 total rcon values for all AES key lengths (rcon list uses 1-based indexing)
        # rcon = [np.zeros(4, dtype="uint8") for _ in range(11)]
        rcon = np.zeros((11, 4), dtype="uint8")
        rcon[1][0] = 1
        for i in range(2, 11):
            rcon[i][0] = (rcon[i - 1][0] << 1) ^ (0x11B & -(rcon[i - 1][0] >> 7))

        # N is the length of the key in 32-bit words (i.e. 4-byte words)
        N = self.key_len // 32
        # R is the number of round keys needed: 11 round keys for AES-128, 13 keys for AES-192, and 15 keys for AES-256
        R = rounds + 1

        # Expanded keys for R rounds in 32-bit words (i.e. 4-byte words)
        # keys = np.asarray([np.zeros(4, dtype="uint8") for _ in range(4 * R)])
        keys = np.zeros((4 * R, 4), dtype="uint8")

        for i in range(4 * R):
            if i < N:
                keys[i] = key[i]
            elif i % N == 0:
                keys_temp = np.zeros((1, 4), dtype="uint8")
                keys_left_shifted = np.zeros((1, 4), dtype="uint8")
                keys_left_shifted = np.roll(keys[i - 1], -1)
                # print("keys_left_shifted.shape: ", keys_left_shifted.shape)
                for ki in range(keys_left_shifted.shape[0]):
                    q_bits = [(keys_left_shifted[ki] >> r) & 1 for r in range(7, -1, -1)]
                    keys_temp[0][ki] = np.uint8(int.from_bytes(AES.bit_transform_gf28(q_bits), byteorder='big'))
                    # keys[i - 1][ki] = AES.bit_transform_gf28(q_bits)
                keys[i] = (keys[i - N] ^ keys_temp[0] ^ rcon[i // N])
                # keys[i] = (keys[i - N] ^ self.S_box[np.roll(keys[i - 1], -1)] ^ rcon[i // N])
            elif (N > 6) and (i % N == 4):
                keys_temp = np.zeros((1, 4), dtype="uint8")
                for ki in range(keys[i-1].shape[1]):
                    q_bits = [(keys[i - 1][ki] >> r) & 1 for r in range(7, -1, -1)]
                    # keys[i - 1][ki] = AES.bit_transform_gf28(q_bits)
                    keys_temp[0][ki] = np.uint8(int.from_bytes(AES.bit_transform_gf28(q_bits), byteorder='big'))
                keys[i] = keys[i - N] ^ keys_temp[0]
                # keys[i] = keys[i - N] ^ self.S_box[keys[i - 1]]
            else:
                keys[i] = keys[i - N] ^ keys[i - 1]

        # Split the keys for each round
        keys = np.split(keys, R)
        # Transpose arrays to match state shape (column-major order) and place in list of keys for each round
        keys = [np.transpose(i) for i in keys]

        # print("keys: ", keys)
        return keys

    def AddRoundKey(self, state, key):
        return np.bitwise_xor(state, key)

    def SubBytes(self, state):
        for j in range(state.shape[1]):
            for i in range(state.shape[0]):
                q_bits = [(state[i][j] >> r) & 1 for r in range(7, -1, -1)]
                # state[i][j] = AES.bit_transform_gf28(q_bits)
                state[i][j] = np.uint8(int.from_bytes(AES.bit_transform_gf28(q_bits), byteorder='big'))
        
        # print("state: ", state)
        return state

    def ShiftRows(self, state):
        return state.take(
            (0, 1, 2, 3, 5, 6, 7, 4, 10, 11, 8, 9, 15, 12, 13, 14)
        ).reshape(4, 4)

    def MixColumns(self, state): # Algorithm for multiplying in Galois Field GF(2^8)
        for i in range(4):
            state[:, i] = self._single_col(state[:, i])
        return state
    
    def _single_col(self, col):
            # col: is a single column of the state
            # col_mixed: is the mixed column to be returned
            # b: does the multiplication by 2 in GF(2^8)
            # Since col is a numpy array, we can perform elementwise operations directly
            x2time = (col << 1) ^ (0x11B & -(col >> 7))

            col_mixed = [
                x2time[0] ^ col[3] ^ col[2] ^ x2time[1] ^ col[1],
                x2time[1] ^ col[0] ^ col[3] ^ x2time[2] ^ col[2],
                x2time[2] ^ col[1] ^ col[0] ^ x2time[3] ^ col[3],
                x2time[3] ^ col[2] ^ col[1] ^ x2time[0] ^ col[0],
            ]

            return col_mixed

    def encrypt(self, plaintext):
        assert len(plaintext) == self.block_size, "Plaintext size must be 128 bits."

        # Create the state
        state = (
            np.frombuffer(plaintext, dtype=np.uint8).reshape((4, 4), order="F").copy()
        )

        # AddRoundKey for initial round
        state = self.AddRoundKey(state=state, key=self.keys[0])
        # print("state: ", state)

        # count=0
        # Rounds 1 to (rounds-1)
        for i in range(1, self.rounds):
            state = self.SubBytes(state=state)
            # count += 1
            # print(f"[{count}]state: ", state)
            state = self.ShiftRows(state=state)
            # print(f"[{count}]state: ", state)
            state = self.MixColumns(state=state)
            # print(f"[{count}]state: ", state)
            state = self.AddRoundKey(state=state, key=self.keys[i])
            # print(f"[{count}]state: ", state)
            # print(f"[{count}]self.keys[i]: ", self.keys[i])

        # Final round
        state = self.SubBytes(state=state)
        state = self.ShiftRows(state=state)
        state = self.AddRoundKey(state=state, key=self.keys[self.rounds])

        ciphertext = state.flatten(order="F")

        return ciphertext
