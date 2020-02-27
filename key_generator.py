import numpy as np
from encryption_helper import EncryptionHelper

class KeyGenerator:

    def __generate_prime_numbers(self):
       return (EncryptionHelper.generate_random_prime_number() for i in range(2))

    def __compute_modulo_number(self, p, q):
        EncryptionHelper.set_N(p * q)
        EncryptionHelper.set_N_squared(np.power(p * q, 2))

    def __generate_sub_matrices(self):
        k1 = EncryptionHelper.create_modular_inverse_matrix(EncryptionHelper.get_N_squared())
        k2, k3, k4 = (EncryptionHelper.generate_random_square_matrix(EncryptionHelper.get_N_squared()) for i in range(3))
        return k1, k2, k3, k4

    def __create_K_matrix(self):
        while True:
            sub_matrices = self.__generate_sub_matrices()
            K_matrix = np.bmat([[sub_matrices[0], sub_matrices[1]],[sub_matrices[2], sub_matrices[3]]])
            if(EncryptionHelper.has_modular_inverse(K_matrix, EncryptionHelper.get_N_squared())):
                return np.matrix(K_matrix,dtype='longlong'), np.matrix(sub_matrices[0],dtype='longlong')

    def generate_secret_key(self):
        p, q = self.__generate_prime_numbers()
        self.__compute_modulo_number(p, q)
        K_matrix, k1_matrix = self.__create_K_matrix()
        k1_inverse = EncryptionHelper.compute_modular_inverse(k1_matrix, EncryptionHelper.get_N_squared())
        K_inverse = EncryptionHelper.compute_modular_inverse(K_matrix, EncryptionHelper.get_N_squared())
        return (k1_matrix, k1_inverse, K_matrix, K_inverse)

