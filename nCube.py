import numpy as np
from numpy.random import uniform, normal
from numpy.linalg import norm


class NCube:
    # A simple class to create a n-dimensional cube and return some useful values.
    def __init__(self, dimensions, length=2, sampleSize=10):
        self.n = dimensions
        self.a = length
        self.sampleSize = sampleSize
        self.samples = None

    @property
    def volume(self):
        return self.a ** self.n

    @property
    def surface(self):
        return 2 * self.n * (self.a ** (self.n - 1))

    def generateUniformSamples(self):
        self.samples = uniform(-self.a / 2, self.a / 2, (self.sampleSize, self.n))

    def generateNormalSamples(self):
        # TODO : Doesn't work for now.
        self.samples = normal(0, self.a / 2, (self.sampleSize, self.n))

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

