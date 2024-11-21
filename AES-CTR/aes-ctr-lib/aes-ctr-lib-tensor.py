from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import torch

def encrypt_aes_ctr(key, data, nonce, counter):
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce, initial_value=counter)
    ct_bytes = cipher.encrypt(data)
    return ct_bytes

def decrypt_aes_ctr(key, nonce, counter, enc_data):
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce, initial_value=counter)
    plaintext = cipher.decrypt(enc_data)
    return plaintext

if __name__ == "__main__":
    # key = get_random_bytes(16)  # Generate a 16-byte key
    key_tensor = torch.tensor([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], dtype=torch.uint8) 
    key = key_tensor.numpy().tobytes()
    print("key_tensor_length(bits): ", len(key_tensor) * 8)
    print("key_tensor: ", key_tensor)
    print("key: ", key)


    # nonce = get_random_bytes(10)  # Generate a 10-byte nonce
    nonce_tensor = torch.tensor([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=torch.uint8) 
    nonce = nonce_tensor.numpy().tobytes()
    print("nonce_tensor: ", nonce_tensor)
    

    # counter = int.from_bytes(get_random_bytes(6), byteorder='big')  # Generate a 6-byte counter
    counter_init = 0
    print("counter_init: ", counter_init)
    counter = counter_init.to_bytes(6, byteorder='big') 

    # Step 1: Create a tensor and convert it to bytes
    tensor = torch.tensor([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], dtype=torch.uint8)    # Replace this with your actual tensor
    data = tensor.numpy().tobytes()
    print("\nOriginal data: ", data)
    print("Original data tensor: ", tensor)

    # Step 2: Encrypt the data
    encrypted_data = encrypt_aes_ctr(key, data, nonce, counter)
    print("\nEncrypted data:", encrypted_data)

    # Step 3: Convert encrypted data back to tensor
    encrypted_tensor = torch.tensor(list(encrypted_data), dtype=torch.uint8)
    print("Encrypted data tensor: ", encrypted_tensor)

    # Step 4: Decrypt the data
    decrypted_data = decrypt_aes_ctr(key, nonce, counter, encrypted_data)
    print("\nDecrypted data: ", decrypted_data)

    # Step 5: Convert decrypted data back to tensor
    decrypted_tensor = torch.tensor(list(decrypted_data), dtype=torch.uint8)
    print("Decrypted data tensor: ", decrypted_tensor)
