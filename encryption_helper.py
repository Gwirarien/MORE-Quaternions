import numpy as np
import random
from math import sqrt
from itertools import count, islice
from pyquaternion import Quaternion

class EncryptionHelper:

    @staticmethod
    def is_prime_number(n):
        if n < 2:
            return False

        for number in islice(count(2), int(sqrt(n) - 1)):
            if n % number == 0:
                return False

        return True

    @staticmethod
    def generate_random_prime_number():
        while True:
            random_number = random.randint(50, 200)
            if(EncryptionHelper.is_prime_number(random_number)):
                return random_number

    @staticmethod
    def signed_modulo(m, p):
        if m >= 0:
            return m % p
        else:
            return -(np.abs(m) % p)

    def __euclidean_algorithm(self, a, b):
        """Extended great common divisor
        returns (gcd(a,b), x, y) such that ax + by = gcd(a,b)"""
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.__euclidean_algorithm(self.signed_modulo(b, a), a)
            return (g, x - (b // a) * y, y)

    @staticmethod
    def inverse_modulo(a, m):
        """Inverse modulo operation"""
        g, x, y = EncryptionHelper.__euclidean_algorithm(a, m)
        if g != 1:
            # If a modular inverse has not been found, break and start again with a new matrix
            raise Exception
        else:
            return EncryptionHelper.signed_modulo(x, m)

    @staticmethod
    def compute_determinant(candidate_matrix):
        a = candidate_matrix[0, 0]
        b = candidate_matrix[0, 1]
        c = candidate_matrix[1, 0]
        d = candidate_matrix[1, 1]
        return (a/100000 * d - b/100000 * c)*100000

    @staticmethod
    def has_inverse(matrix):
        determinant = EncryptionHelper.compute_determinant(matrix)
        if determinant != 0:
            return True

    @staticmethod
    def compute_inverse_matrix(determinant, matrix, mod_value):
        """Computes the inverse of a 2x2 matrix"""
        inv_determinant = EncryptionHelper.inverse_modulo(determinant, mod_value)

        inverse_matrix = np.zeros(2,2)
        inverse_matrix[0, 0] = matrix[1, 1]
        inverse_matrix[0, 1] = -matrix[0, 1]
        inverse_matrix[1, 0] = -matrix[1, 0]
        inverse_matrix[1, 1] = matrix[0, 0]

        return inv_determinant * inverse_matrix

    @staticmethod
    def generate_random_square_matrix(mod_value):
        matrix = (np.random.rand(2,2)*1000000000).astype(int)
        return matrix % mod_value

    @staticmethod
    def create_quaternion(sigma, mod_value):
        alfa, beta, gamma = (EncryptionHelper.signed_modulo(random.randint(1, 100000000), mod_value) for i in range(3))
        return Quaternion(sigma, alfa*mod_value, beta*mod_value, gamma*mod_value)



