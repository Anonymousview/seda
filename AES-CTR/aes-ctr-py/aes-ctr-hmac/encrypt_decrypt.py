from aes import AES
from ctr import CTR
import getpass 
import secrets
import argparse
import hmac 
import hashlib 


def encrypt_decrypt(func, in_stream, block_size, count_start):
    return b"".join(
        [
            func(in_stream[i : i + block_size], i // block_size + count_start)
            for i in range(0, len(in_stream), block_size)
        ]
    )

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--encrypt", action="store_true")
    group.add_argument("-d", "--decrypt", action="store_true")
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    args = parser.parse_args()

    passwd = getpass.getpass(
        "Enter {} password: ".format("encryption" if args.encrypt else "decryption")
    )

    block_size = 16 # AES block size is 16 bytes = 128 bits

    # Read input file
    with open(args.input_file, "rb") as f:
        file_in = f.read()

    # Encryption
    if args.encrypt:
        # Create a random 128 bit salt (16 bytes) used in the key derivation function
        # The salt will be stored as the first block of the ciphertext
        # salt = secrets.token_bytes(block_size) # random bytes of block_size 
        salt = b'\x00' * block_size

        # Generate a random 10 bytes nonce by definition of CTR mode
        # nonce = secrets.token_bytes(10)
        nonce = b'\x0F' * 10

        # Create the IV from the nonce and the initial 6-byte counter value of 0
        # The IV will be stored as the second block of the ciphertext
        counter = 0
        IV = nonce + counter.to_bytes(6, byteorder="big") # connect nonce and counter

        # Start the AES cipher 
        cipher = AES(password_str=passwd, salt=salt, key_len=256)
        # Start the CTR mode
        mode = CTR(cipher, nonce)

        # Encrypt the file and write to output file
        file_out = (
            salt + IV + encrypt_decrypt(mode.encrypt, file_in, block_size, counter)
        )

        # Create authentication HMAC and store it as the last two blocks of the file
        hmac_val = hmac.digest(key=cipher.hmac_key, msg=file_out, digest=hashlib.sha256) # 256 bits

        # Append HMAC to the ciphertext
        file_out += hmac_val

    # Decryption
    else:
        # Read the salt from the first block of the ciphertext
        salt = file_in[:block_size]

        # Read the IV from the second block of the ciphertext: nonce is the first 10 bytes, counter is the next 6 bytes
        IV = file_in[block_size : block_size * 2]
        nonce = IV[:10]
        counter = int.from_bytes(IV[10:], byteorder="big")

        # Read the HMAC from the last two blocks of the ciphertext
        hmac_val = file_in[-2 * block_size:]

        # Start the AES cipher
        cipher = AES(password_str=passwd, salt=salt, key_len=256)

        # Compare it to the stored HMAC
        assert hmac.compare_digest(
            hmac_val,
            hmac.digest(key=cipher.hmac_key, msg=file_in[:-2 * block_size], digest=hashlib.sha256),
        ), "HMAC does not match!"

        # Start the CTR mode
        mode = CTR(cipher, nonce)

        # Skip the salt, IV, and HMAC blocks and decrypt the rest of the file
        file_in = file_in[2 * block_size : -2 * block_size]

        file_out = encrypt_decrypt(mode.decrypt, file_in, block_size, counter)

    # Write output file
    with open(args.output_file, "wb") as f:
        f.write(file_out)

    print("\n{0}operation successful! {1} has been stored in {2}".format(
        "Encryption" if args.encrypt else "Decryption",
        "Ciphertext" if args.encrypt else "Plaintext",
        args.output_file
    ))

if __name__ == "__main__": 
    main()    
