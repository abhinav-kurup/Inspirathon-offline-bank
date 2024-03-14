import base64
import jwt
from Crypto.Cipher import AES
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes



def aes_decrypt(encrypted_data):
    # Decode the secret key from base64
    print(len(encrypted_data))
    encrypted_data_bytes = base64.b64decode(encrypted_data)
    secret_key = "YUI1YVBjIzhRMnJEZkc5TGhNN1p4WXROMXZXM2tFNko="
    secret_key_bytes = base64.b64decode(secret_key)
    # secret_key_bytes = b"\xe0P\xc0\xb6'\xb9\x7f\x9e\xe9\x1fU\xc9\t\x04t\xc51\xa4\xad=\x04Qu\x99\xc1;]\x0f\xc1HT*"
    print("Secret Key: ")
    # Split the IV (Initialization Vector) and encrypted data
    iv = encrypted_data_bytes[:16]  # Assuming a 16-byte IV
    ciphertext = encrypted_data_bytes[16:]
    
    # Create a Cipher object
    cipher = Cipher(algorithms.AES(secret_key_bytes), modes.CBC(iv))
    # Create a decryptor object
    decryptor = cipher.decryptor()
    print("hello1")
    # Perform the decryption
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    print(decrypted_data)
    base64_encoded_str = base64.b64encode(decrypted_data).decode('utf-8')
    return base64_encoded_str


def aes_dec(encrypted_data):
    # Extract the IV and ciphertext
    secret_key = "bXkgMzIgbGVuZ3RoIGtleS4uLi4uLi4uLi4uLi4uLi4="
    secret_key_b= base64.b64decode(secret_key)
    enc_data_b=base64.b64decode(encrypted_data)
    print(enc_data_b)
    iv = enc_data_b[:16]
    ciphertext = enc_data_b[16:]
    print(ciphertext)
    # Create a Cipher object
    cipher = AES.new(secret_key_b, AES.MODE_CFB, iv)

    # Create a decryptor object
    decryptor = cipher.decrypt(ciphertext)
    print(decryptor)
    # Perform the decryption
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    print(decrypted_data)
    print(type(decrypted_data))
    return decrypted_data.decode('utf-8')

def jwt_dec(data):
    secret_key = 'my_secret_key'  
    print("hello")
    decoded_token = jwt.decode(data, secret_key, algorithms=['HS256'])
    print(decoded_token)
    return decoded_token

def jwt_enc(data):
    secret_key = 'my_secret_key'  
    print("hello")
    decoded_token = jwt.encode(data, secret_key,  algorithm='HS256')
    print(decoded_token)
    return decoded_token