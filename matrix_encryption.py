import numpy as np
import random
from encryption_helper import EncryptionHelper

class MatrixEncryption:

    def __convert_message(self, message):
        return EncryptionHelper.signed_modulo(message, EncryptionHelper.get_N_squared())

    def __create_first_message_matrix(self, m):
        r1, r2 = (random.randint(1, 1000)%EncryptionHelper.get_N_squared() for i in range(2))
        return np.array([[m, r1],[0, r2]])

    def __create_second_message_matrix(self, m_1):
        r1_1 = random.randint(1, 1000)%EncryptionHelper.get_N_squared()
        return np.array([[m_1, r1_1], [0, 0]])

    def __create_message_sub_matrices(self, secret_key, message):
        m = EncryptionHelper.create_quaternion(message, EncryptionHelper.get_N())
        M = self.__create_first_message_matrix(m)
        M_1 = np.matrix((secret_key[0].dot(M)).dot(secret_key[1]))
        m_1 = EncryptionHelper.create_quaternion(message, EncryptionHelper.get_N())
        M_2 = self.__create_second_message_matrix(m_1)
        return M_1, M_2

    def encrypt_message(self, secret_key, message):
        converted_message = self.__convert_message(message)
        M_1, M_2 = self.__create_message_sub_matrices(secret_key, converted_message)
        R = EncryptionHelper.generate_random_square_matrix(EncryptionHelper.get_N_squared())
        M_final = np.matrix(np.bmat([[M_1, R],[np.zeros([2,2]), M_2]]))
        return np.matrix((secret_key[2].dot(M_final)).dot(secret_key[3]))
