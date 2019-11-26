import numpy as np
import random

class MatrixDecryption:

    __N = random.randint(1,100000)

    def __init__(self, obj):
        self.__N = obj.get_N()
        self.__N_squared = obj.get_N_squared()

    def __recreate_M_1_matrix(self, matrix):
        return np.matrix([[matrix[0, 0], matrix[0, 1]],
                          [matrix[1, 0], matrix[1, 1]]])

    def __recreate_M_2_matrix(self, matrix):
        return np.matrix([[matrix[2, 2], matrix[2, 3]],
                          [matrix[3, 2], matrix[3, 3]]])

    def __check_result(self, M, M2, verifiable):
        m = M.real%self.__N_squared
        if(verifiable):
            m1 = M2.real % self.__N_squared
            if (m == m1):
                return m
            else:
                return None
        return m

    def decrypt_message(self, secret_key, encrypted_matrix):
        rebuilt_message_matrix = np.matrix(secret_key[3].dot((encrypted_matrix).dot(secret_key[2])))
        M_2 = self.__recreate_M_2_matrix(rebuilt_message_matrix)
        M_1 = self.__recreate_M_1_matrix(rebuilt_message_matrix)
        M = np.matrix(secret_key[1].dot((M_1).dot(secret_key[0])))
        return self.__check_result(M[0, 0], M_2[0, 0], False)
