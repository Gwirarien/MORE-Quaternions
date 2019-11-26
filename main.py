from key_generator import KeyGenerator
from matrix_encryption import MatrixEncryption
from matrix_decryption import MatrixDecryption
from encryption_helper import EncryptionHelper
import numpy as np
import sys

def not_found_message():
    print("Value not found")
    raise Exception

key_gen = KeyGenerator()
message = 3
message1 = 5

retries = 0
is_not_found = True

while is_not_found:
    try:
        secret_key = key_gen.generate_secret_key()

        count = 0
        while True:
            encrypted_matrix = MatrixEncryption(key_gen).encrypt_message(secret_key, message)
            decrypted_message = MatrixDecryption(key_gen).decrypt_message(secret_key, encrypted_matrix)

            if (decrypted_message != message):
                secret_key = key_gen.generate_secret_key() # If the key is regenerated every iteration, the chances of a correct encryption/decryption rises
                count += 1
            elif (decrypted_message == message):
                print("The message {0} was recovered after {1} iterations out of 1000".format(decrypted_message, count))
                break
            if(count > 1000):
                not_found_message()

        count = 0
        while True:
            encrypted_matrix_1 = MatrixEncryption(key_gen).encrypt_message(secret_key, message1)
            encrypted_matrix_2 = MatrixEncryption(key_gen).encrypt_message(secret_key, message1)
            N_squared = key_gen.get_N_squared()
            encrypted_matrix_2 = EncryptionHelper.mod_quaternion_matrix(encrypted_matrix_2, N_squared)
            sum_matrix = np.add(encrypted_matrix_1, encrypted_matrix_2)
            decrypted_message = MatrixDecryption(key_gen).decrypt_message(secret_key, sum_matrix)
            if (decrypted_message != (message + message1)):
                count += 1
            elif (decrypted_message == (message + message1)):
                print("The sum {0} was recovered after {1} iterations out of 1000".format(decrypted_message, count))
                break
            if(count > 1000):
                not_found_message()

        count = 0
        while True:
            encrypted_matrix_1 = MatrixEncryption(key_gen).encrypt_message(secret_key, message)
            encrypted_matrix_2 = MatrixEncryption(key_gen).encrypt_message(secret_key, message1)
            N_squared = key_gen.get_N_squared()
            encrypted_matrix_2 = EncryptionHelper.mod_quaternion_matrix(encrypted_matrix_2, N_squared)
            product_matrix = encrypted_matrix_1.dot(encrypted_matrix_2)
            decrypted_message = MatrixDecryption(key_gen).decrypt_message(secret_key, product_matrix)

            if (decrypted_message != (message * message1)):
                count += 1
            elif (decrypted_message == (message * message1)):
                print("The multiplication {0} was recovered after {1} iterations out of 1000".format(decrypted_message, count))
                break
            if(count > 1000):
                not_found_message()

        is_not_found = False
    except:
        retries += 1
        print("Retrying")

        if(retries > 30):
            print("Number of retries exceeded")
            sys.exit()
        pass

print("The messages were decrypted correctly after {0} retries".format(retries))