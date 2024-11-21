import hashlib

def calculate_sha256(input_string: str) -> str:
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))

    return sha256_hash.hexdigest()

if __name__ == "__main__":
    message = "Hello, World!"
    # print(f"SHA-256: {calculate_sha256(message)}")
    print(f"[hashlib] SHA-256 of '{message}': {calculate_sha256(message)}")
