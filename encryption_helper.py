import numpy as np
import sympy as sp
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
            random_number = random.randint(2, 5) # TODO: find a way to support larger values
            if(EncryptionHelper.is_prime_number(random_number)):
                return random_number

    @staticmethod
    def signed_modulo(m, p):
        if m >= 0:
            return m % p
        else:
            return -(np.fmod(np.abs(m), p))

    @staticmethod
    def inverse_modulo(a, m):
        a = EncryptionHelper.signed_modulo(a, m);
        for x in range(1, m):
            if (EncryptionHelper.signed_modulo((a*x), m) == 1):
                return x
        return 1 #No inverse mod

    @staticmethod
    def has_inverse(matrix):
        determinant = np.linalg.det(matrix)
        if determinant != 0:
            return True

    @staticmethod
    def matrix_minor(matrix, i, j):
        return np.delete(np.delete(matrix, i, axis=0), j, axis=1)

    @staticmethod
    def compute_modular_inverse(matrix, mod_value):
        size = len(matrix)
        adj = np.zeros(shape=(size, size))
        determinant = int(round(np.linalg.det(matrix)))
        for i in range(0, size):
            for j in range(0, size):
                sign = (-1)**(i+j)
                minor = EncryptionHelper.matrix_minor(matrix, j, i)
                adj[i][j] = (sign*int(round(np.linalg.det(minor))))%mod_value
        return np.matrix((EncryptionHelper.inverse_modulo(determinant, mod_value) * adj)%mod_value,dtype='longlong')

    @staticmethod
    def has_modular_inverse(matrix, mod_value):
        try:
            determinant = np.linalg.det(matrix)
            if ((determinant != 0) and (EncryptionHelper.inverse_modulo(round(determinant), mod_value) != 1)):
                return True #investigate if a 4x4 matrix is correctly calculated
        except:
            return False

    @staticmethod
    def create_modular_inverse_matrix(mod_value):
        while True:
            matrix = EncryptionHelper.generate_random_square_matrix(mod_value)
            try:
                if(EncryptionHelper.has_modular_inverse(matrix, mod_value)):
                    return matrix
            except:
                pass

    @staticmethod
    def generate_random_square_matrix(mod_value):
        matrix = (np.random.rand(2,2)*1000).astype('longlong')
        return matrix % mod_value

    @staticmethod
    def create_quaternion(sigma, mod_value):
        alfa, beta, gamma = (random.randint(1, 1000)%mod_value for i in range(3))
        return Quaternion(sigma, alfa*mod_value, beta*mod_value, gamma*mod_value)
