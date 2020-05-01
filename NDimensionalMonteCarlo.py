import numpy as np
from nBall import NBall
from nCube import NCube


class NDimensionalMonteCarlo:
    def __init__(self, dimensions, radius=1, length=2):
        self.dimensions = dimensions
        self.nBall = NBall(dimensions, radius)
        self.nCube = NCube(dimensions, length)
        self.volume = None

    def nBallVolumeUniformSample(self, sampleSize=10000):
        self.nCube.generateUniformSamples(sampleSize)
        norms = self.nCube.generateNorms

        conditions = norms[:] <= self.nBall.r
        results = norms[conditions]

        self.volume = (len(results) / sampleSize) * self.nCube.volume
        return self.volume

    @property
    def difference(self):
        return self.volume - self.nBall.volume
