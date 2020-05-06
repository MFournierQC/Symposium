import numpy as np
from numpy.random import uniform, rand
from numpy.linalg import norm


class NCube:
    # A simple class to create a n-dimensional cube and return some useful values.
    def __init__(self, dimensions, length=2):
        self.dimensions = dimensions
        self.a = length

        self.volume = self.a ** self.dimensions
        self.surface = 2 * self.dimensions * (self.a ** (self.dimensions - 1))

        self.samples = None

    def uniformSample(self, sampleSize=10000):
        self.samples = uniform(-self.a / 2, self.a / 2, (sampleSize, self.dimensions))

    def uniformLatinHypercubeSample(self, sampleSize=10000):
        interval = np.linspace(0, 1, sampleSize + 1)

        uniformDistribution = rand(sampleSize, self.dimensions)
        lower = interval[:sampleSize]
        upper = interval[1:sampleSize + 1]
        rdpoints = np.zeros_like(uniformDistribution)
        for i in range(self.dimensions):
            rdpoints[:, i] = uniformDistribution[:, i] * (upper - lower) + lower

        uniformSample = np.zeros_like(rdpoints)
        for i in range(self.dimensions):
            order = np.random.permutation(range(sampleSize))
            uniformSample[:, i] = rdpoints[order, i]

        self.samples = (uniformSample * self.a) - self.a / 2

    @property
    def generateNorms(self):
        if self.samples is not None:
            return np.array([norm(sample) for sample in self.samples])
        else:
            raise TypeError('Samples have not been generated.')

    @property
    def randomCoordinates(self):
        return uniform(-self.a / 2, self.a / 2, self.dimensions)

    @property
    def randomNorm(self):
        return norm(self.randomCoordinates)

