import numpy as np
from numpy.random import uniform
from numpy.linalg import norm


class NCube:
    # A simple class to create a n-dimensional cube and return some useful values.
    def __init__(self, dimensions, length=2):
        self.n = dimensions
        self.a = length

    @property
    def volume(self):
        return self.a ** self.n

    @property
    def surface(self):
        return 2 * self.n * (self.a ** (self.n - 1))

    @property
    def randomCoordinates(self):
        return uniform(-self.a / 2, self.a / 2, self.n)

    @property
    def randomNorm(self):
        return norm(self.randomCoordinates)

