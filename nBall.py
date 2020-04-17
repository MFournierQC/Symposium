import numpy as np
from scipy.special import gamma


class NBall:
    def __init__(self, dimensions, radius=1):
        self.n = dimensions
        self.r = radius

    @property
    def volume(self):
        return (np.pi ** (self.n / 2)) / (gamma((self.n / 2) + 1)) * (self.r ** self.n)

    @property
    def surface(self):
        return (2 * (np.pi ** ((self.n + 1) / 2))) / (gamma((self.n + 1) / 2)) * (self.r ** self.n)
