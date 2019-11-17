from key_generator import KeyGenerator
from matrix_encryption import MatrixEncryption
from matrix_decryption import MatrixDecryption
import numpy as np
import sys
import time


def not_found_message():
    print("Value not found")
    time.sleep(2)
    raise Exception

key_gen = KeyGenerator()

message_sigma = 20
message1_sigma = 10

retries = 0
is_not_found = True

while is_not_found:
    try:
        secret_key = key_gen.generate_secret_key()

        count = 0
        while True:
            encrypted_matrix = MatrixEncryption(key_gen).encrypt_message(secret_key, message_sigma)
            decrypted_message = MatrixDecryption(key_gen).decrypt_message(secret_key, encrypted_matrix)

            if (decrypted_message != message_sigma):
                count = count + 1
            elif (decrypted_message == message_sigma):
                print("The value {0} was found after {1} iterations".format(decrypted_message, count))
                break
            if(count > 1000):
                not_found_message()

        count = 0
        while True:
            encrypted_matrix = MatrixEncryption(key_gen).encrypt_message(secret_key, message_sigma)
            encrypted_matrix1 = MatrixEncryption(key_gen).encrypt_message(secret_key, message1_sigma)
            sum_matrix = np.add(encrypted_matrix, encrypted_matrix1)
            decrypted_message = MatrixDecryption(key_gen).decrypt_message(secret_key, sum_matrix)

            if (decrypted_message != (message_sigma+message1_sigma)):
                count = count + 1
            elif (decrypted_message == (message_sigma+message1_sigma)):
                print("The result {0} was found after {1} iterations".format(decrypted_message, count))
                break
            if(count > 1000):
                not_found_message()

        count = 0
        while True:
            encrypted_matrix = MatrixEncryption(key_gen).encrypt_message(secret_key, message_sigma)
            encrypted_matrix1 = MatrixEncryption(key_gen).encrypt_message(secret_key, message1_sigma)
            subtraction_matrix = np.subtract(encrypted_matrix, encrypted_matrix1)
            decrypted_message = MatrixDecryption(key_gen).decrypt_message(secret_key, subtraction_matrix)

            if (decrypted_message != (message_sigma-message1_sigma)):
                count = count + 1
            elif (decrypted_message == (message_sigma-message1_sigma)):
                print("The subtraction {0} was found after {1} iterations".format(decrypted_message, count))
                break
            if(count > 1000):
                not_found_message()

        is_not_found = False
    except:
        retries += 1
        print("Retrying")

        if(retries > 10):
            print("Retries exceeded")
            sys.exit()
        pass

print("The messages were decrypted correctly after {0} retries".format(retries))