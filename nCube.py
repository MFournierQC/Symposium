import numpy as np
from numpy.random import uniform, normal
from numpy.linalg import norm


class NCube:
    # A simple class to create a n-dimensional cube and return some useful values.
    def __init__(self, dimensions, length=2):
        self.n = dimensions
        self.a = length

        self.volume = self.a ** self.n
        self.surface = 2 * self.n * (self.a ** (self.n - 1))

        self.samples = None

    def generateUniformSamples(self, sampleSize=10000):
        self.samples = uniform(-self.a / 2, self.a / 2, (sampleSize, self.n))

    @property
    def generateNorms(self):
        if self.samples is not None:
            return np.array([norm(sample) for sample in self.samples])
        else:
            raise TypeError('Samples have not been generated.')

    @property
    def randomCoordinates(self):
        return uniform(-self.a / 2, self.a / 2, self.n)

    @property
    def randomNorm(self):
        return norm(self.randomCoordinates)

