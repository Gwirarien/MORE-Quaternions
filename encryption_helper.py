import numpy as np
import sympy as sp
import random
from math import sqrt
from itertools import count, islice
from pyquaternion import Quaternion

class EncryptionHelper:

    __N = random.randint(1000, 10000)
    __N_squared = random.randint(1000, 10000)

    @staticmethod
    def set_N(value):
        EncryptionHelper.__N = value

    @staticmethod
    def set_N_squared(value):
        EncryptionHelper.__N_squared = value

    @staticmethod
    def get_N():
        return EncryptionHelper.__N

    @staticmethod
    def get_N_squared():
        return EncryptionHelper.__N_squared

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
            random_number = random.randint(2, 5) # Workaround to prevent overflow
            if(EncryptionHelper.is_prime_number(random_number)):
                return random_number

    @staticmethod
    def exponential(n, x):
        sum = 1.0
        for i in range(n, 0, -1):
            sum = 1 + x * sum / i
        return sum

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
                return True
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
    def mod_quaternion_matrix(matrix, N):
        mod_matrix = np.array([])
        for i in range(4):
            for j in range(4):
                quaternion = matrix[j, i]
                quaternion[0] = quaternion[0] % N
                quaternion[1] = quaternion[1] % N
                quaternion[2] = quaternion[2] % N
                quaternion[3] = quaternion[3] % N
                mod_quaternion = Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3])
                mod_matrix = np.append(mod_matrix, mod_quaternion)
        return np.reshape(np.matrix(mod_matrix), (4, 4))

    @staticmethod
    def generate_random_square_matrix(mod_value):
        matrix = (np.random.rand(2,2)*1000).astype('longlong')
        return matrix % mod_value

    @staticmethod
    def create_quaternion(sigma, mod_value):
        alfa, beta, gamma = (random.randint(1, 1000)%mod_value for i in range(3))
        return Quaternion(sigma, alfa*mod_value, beta*mod_value, gamma*mod_value)
