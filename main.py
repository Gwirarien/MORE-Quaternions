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
factor = 10**3

message = 0.01243
message_scaled = round(message*factor)

message1 = 0.00417
message1_scaled = round(message1*factor)


retries = 0
is_not_found = True

while is_not_found:
    try:
        secret_key = key_gen.generate_secret_key()
        encrypted_matrix = MatrixEncryption().encrypt_message(secret_key, message_scaled)

        count = 0
        while True:
            encrypted_matrix = MatrixEncryption().encrypt_message(secret_key, message_scaled)
            decrypted_message = MatrixDecryption().decrypt_message(secret_key, encrypted_matrix, False)

            if (decrypted_message != message_scaled):
                secret_key = key_gen.generate_secret_key() # If the key is regenerated every iteration, the chances of a correct encryption/decryption rises
                count += 1
            elif (decrypted_message == message_scaled):
                print("The message {0} was recovered after {1} iterations out of 1000".format(decrypted_message/factor, count))
                break
            if(count > 1000):
                not_found_message()

        count = 0
        while True:
            encrypted_matrix_1 = MatrixEncryption().encrypt_message(secret_key, message_scaled)
            encrypted_matrix_2 = MatrixEncryption().encrypt_message(secret_key, message1_scaled)
            N_squared = EncryptionHelper.get_N_squared()
            encrypted_matrix_2 = EncryptionHelper().mod_quaternion_matrix(encrypted_matrix_2, N_squared)
            sum_matrix = np.add(encrypted_matrix_1, encrypted_matrix_2)
            decrypted_message = MatrixDecryption().decrypt_message(secret_key, sum_matrix, False)

            if (decrypted_message != (message_scaled + message1_scaled)):
                count += 1
            elif (decrypted_message == (message_scaled + message1_scaled)):
                print("The sum {0} was recovered after {1} iterations out of 1000".format(decrypted_message/factor, count))
                break
            if (count > 1000):
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