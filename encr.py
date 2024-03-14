import base64
import jwt
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Generate a random AES key as bytes (256 bits / 32 bytes)
def generate_aes_key():
    key = os.urandom(32)  # Generate a 32-byte (256-bit) AES key
    return key

# Encrypt data using the generated secret key
def aes_encrypt(data, secret_key):
    # Generate a random IV (Initialization Vector)
    iv = os.urandom(16)  # 16 bytes for AES-128 or AES-256

    # Create a Cipher object
    cipher = Cipher(algorithms.AES(secret_key), modes.CFB(iv))

    # Create an encryptor object
    encryptor = cipher.encryptor()

    # Perform the encryption
    encrypted_data = encryptor.update(data.encode('utf-8')) + encryptor.finalize()

    # Combine IV and ciphertext
    encrypted_data = iv + encrypted_data

    return encrypted_data

# Decrypt data using the generated secret key
def aes_decrypt(encrypted_data, secret_key):
    # Extract the IV and ciphertext
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]

    # Create a Cipher object
    cipher = Cipher(algorithms.AES(secret_key), modes.CFB(iv))
    print(cipher)
    # Create a decryptor object
    decryptor = cipher.decryptor()

    # Perform the decryption
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    print(decrypted_data)
    return decrypted_data.decode('utf-8')

# Example usage:



# Convert the bytes key to a base64-encoded string
secret_key = "bXkgMzIgbGVuZ3RoIGtleS4uLi4uLi4uLi4uLi4uLi4="
print("Secret Key:", secret_key)
aes_key_bytes = base64.b64decode(secret_key)
# Data to encrypt
plaintext = "my name is khanjsv jen  jehfhkghWUGHUHREUWE"

# Encrypt the data
encrypted_data = aes_encrypt(plaintext, aes_key_bytes)
print("Encrypted Data:", encrypted_data)

# Convert the encrypted data to a base64-encoded string
encrypted_data_str = base64.b64encode(encrypted_data).decode('utf-8')
print("Encrypted Data (Base64 String):", encrypted_data_str)

# Decrypt the data
decrypted_data = aes_decrypt(base64.b64decode(encrypted_data_str), aes_key_bytes)
print("Decrypted Data:", decrypted_data)


def jwt_decode(data):
    jwt_token = jwt.decode(data, verify=False)
    return jwt_token