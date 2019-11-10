import numpy as np
import random
from encryption_helper import EncryptionHelper

class MatrixDecryption:

    __N = random.randint(1,100000)

    def __init__(self, obj):
        # TODO: find another way to pass the __N and __N_squared args
        self.__N = obj.get_N()
        self.__N_squared = obj.get_N_squared()

    def decrypt_message(self, secret_key, encrypted_matrix):
        rebuilt_message_matrix = (secret_key[3].dot(encrypted_matrix)).dot(secret_key[2])
        M_1 = np.array([[rebuilt_message_matrix[0,0], rebuilt_message_matrix[0,1]],[rebuilt_message_matrix[1,0], rebuilt_message_matrix[1,1]]])
        M = secret_key[1].dot(M_1).dot(secret_key[0])
        m = M[1,1]
        m_1 = M_1[1,1]
        print(m.real%self.__N, m_1.real%self.__N)