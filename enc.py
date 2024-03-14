from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes
import base64

# The encrypted data in base64 format
encrypted_data_base64 = "rSTBBvKSYYe8jGBoX1n7nQ=="

# The secret key
secret_key = "my 32 length key................"

# Decode the secret key from UTF-8
secret_key_bytes = secret_key.encode('utf-8')
print("Hello")
# Decode the base64-encoded encrypted data
encrypted_data = base64.b64decode(encrypted_data_base64)
print(encrypted_data)
# Split the IV (Initialization Vector) and ciphertext
iv = encrypted_data[:16]  # Assuming a 16-byte IV
ciphertext = encrypted_data[16:]
print("okay")
# Create a Cipher object for decryption
cipher = AES.new(secret_key_bytes, AES.MODE_CFB, iv)
print("okay1")
# Decrypt the ciphertext
decrypted_data_bytes = cipher.decrypt(ciphertext)
print(decrypted_data_bytes)
# Unpad the decrypted data (if padding was used during encryption)
# You need to know the padding scheme used during encryption to correctly unpad
# In this example, 'null' padding was used, which means you may not need to unpad
# If padding is not used, you may need to adjust this step accordingly
# unpadded_data = unpad(decrypted_data_bytes, AES.block_size)
print("okay3")
# Convert the result to a string
decrypted_data_str = decrypted_data_bytes.decode('utf-8')
print("okay4")
# Print the decrypted data
print("Decrypted Data:", decrypted_data_str)
