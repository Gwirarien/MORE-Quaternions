import numpy as np
import random
from encryption_helper import EncryptionHelper

class MatrixDecryption:

    __N = random.randint(1,100000)

    def __init__(self, obj):
        # TODO: find another way to pass the __N and __N_squared args
        self.__N = obj.get_N()
        self.__N = obj.get_N_squared()

    def decrypt_message(self, secret_key, encrypted_matrix):
        rebuilt_message_matrix = secret_key[3].dot((encrypted_matrix)/100000).dot(secret_key[2])*100000
        M_1 = np.array([[rebuilt_message_matrix[0,0], rebuilt_message_matrix[0,1]],[rebuilt_message_matrix[1,0], rebuilt_message_matrix[1,1]]])
        M = secret_key[1].dot((M_1)/100000).dot(secret_key[0])*100000
        m = M[1,1]
        m_1 = M_1[1,1]
        print(EncryptionHelper.signed_modulo((m.real), self.__N), EncryptionHelper.signed_modulo((m_1.real), self.__N))