from key_generator import KeyGenerator
from matrix_encryption import MatrixEncryption
from matrix_decryption import MatrixDecryption

key_gen = KeyGenerator()
secret_key = key_gen.generate_secret_key()

message_sigma = 10

while True:
    encrypted_matrix = MatrixEncryption(key_gen).encrypt_message(secret_key, message_sigma)
    decrypted_message = MatrixDecryption(key_gen).decrypt_message(secret_key, encrypted_matrix)
    if(decrypted_message):
        break

print(decrypted_message)
