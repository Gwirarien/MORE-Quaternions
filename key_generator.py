import numpy as np
import random
from encryption_helper import EncryptionHelper

class KeyGenerator:

    __N = random.randint(1000, 10000)
    __N_squared = random.randint(1000, 10000)

    def get_N(self):
        return self.__N

    def get_N_squared(self):
        return self.__N_squared

    def __generate_prime_numbers(self):
       return (EncryptionHelper.generate_random_prime_number() for i in range(2))

    def __compute_modulo_number(self, p, q):
        self.__N = p * q
        self.__N_squared = np.power(self.__N, 2)


    def __generate_sub_matrices(self):
        k1, k2, k3, k4 = (EncryptionHelper.generate_random_square_matrix(self.__N_squared) for i in range(4))
        for i in k1, k2, k3, k4:
            if(EncryptionHelper.has_inverse(i)):
                k1, i = i, k1
                matrices = k1, k2, k3, k4
                return matrices
            else:
                self.__generate_sub_matrices()

    def __create_K_matrix(self):
        while True:
            sub_matrices = self.__generate_sub_matrices()
            K_matrix = np.bmat([[sub_matrices[0], sub_matrices[1]],[sub_matrices[2], sub_matrices[3]]])
            if(np.linalg.det(K_matrix) != 0):
                return K_matrix, sub_matrices[0]

    def generate_secret_key(self):
        p, q = self.__generate_prime_numbers()
        self.__compute_modulo_number(p, q)
        K_matrix, k1_matrix = self.__create_K_matrix()
        return (k1_matrix, np.linalg.inv(k1_matrix), K_matrix, np.linalg.inv(K_matrix))





