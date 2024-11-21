from aes_gf import AES
# from aes_lookup import AES
from ctr import CTR
import secrets 
import argparse 
import torch 


def encrypt_decrypt(func, in_stream, block_size, count_start):
    return b"".join(
        [
            func(in_stream[i : i + block_size], i // block_size + count_start)
            for i in range(0, len(in_stream), block_size)
        ]
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", action="store_true", help="Encrypt")
    parser.add_argument("-d", action="store_true", help="Decrypt")
    args = parser.parse_args()

    block_size = 16 # AES block size is 16 bytes = 128 bits

    # Create a tensor and convert it to bytes
    # tensor_data = torch.tensor([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], dtype=torch.uint8) 
    tensor_data = torch.tensor([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], dtype=torch.uint8) 
    print("Original data: ", tensor_data) 
    data_in = tensor_data.numpy().tobytes()

    key_len = 128 # AES key length
    # random 
    key = secrets.token_bytes(key_len // 8) # Generate a random 32-byte key
    key_tensor = torch.tensor(list(key), dtype=torch.uint8)
    # initial
    key_tensor = torch.tensor([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], dtype=torch.uint8)
    key = key_tensor.numpy().tobytes()

    print("\nkey_tensor_length(bits): ", len(key_tensor) * 8)
    print("key: ", key)
    print("key_tensor: ", key_tensor)
    
    

    # IV = nonce + counter. nonce is the first 10 bytes, counter is the next 6 bytes
    # nonce = b'\x0F' * 10 # Generate a random 10-byte nonce
    # random 
    nonce = secrets.token_bytes(10) # Generate a random 10-byte nonce
    nonce_tensor = torch.tensor(list(nonce), dtype=torch.uint8)
    # initial
    nonce_tensor = torch.tensor([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=torch.uint8) 
    nonce = nonce_tensor.numpy().tobytes()

    print("\nnonce: ", nonce)
    print("nonce_tensor: ", nonce_tensor)


    # Encryption
    if args.e:
        counter = 0
        IV = nonce + counter.to_bytes(6, byteorder="big") # connect nonce and counter

        # Start the AES cipher 
        cipher = AES(key=key, key_len=key_len)
        # Start the CTR mode
        mode = CTR(cipher, nonce)

        ciphertext_out = encrypt_decrypt(mode.encrypt, data_in, block_size, counter)

        print("\n{0} operation successful! ".format(
        "Encryption" if args.e else "Decryption"))

        # Convert decrypted data back to tensor
        encrypted_tensor = torch.tensor(list(ciphertext_out), dtype=torch.uint8)
        print("Encrypted tensor: ", encrypted_tensor)


    # Decryption
    if args.d:
        counter = 0
        IV = nonce + counter.to_bytes(6, byteorder="big") # connect nonce and counter

        cipher = AES(key=key, key_len=key_len)
        mode = CTR(cipher, nonce)

        if args.e:
            file_out = encrypt_decrypt(mode.decrypt, ciphertext_out, block_size, counter)
        else:
            file_out = encrypt_decrypt(mode.decrypt, data_in, block_size, counter)

        print("\n{0} operation successful! ".format(
        "Decryption" if args.d else "Encryption"))

        decrypted_tensor = torch.tensor(list(file_out), dtype=torch.uint8)
        print("Decrypted tensor: ", decrypted_tensor)


if __name__ == "__main__": 
    main()    
