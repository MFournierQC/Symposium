import numpy as np
from nBall import NBall
from nCube import NCube


class MonteCarlo:
    def __init__(self):
        self.nBall = None
        self.nCube = None

        self.volume = None

    def nBallVolume(self, dimensions, cubeLength=2, sphereRadius=1, sampleSize=10000):
        self.nBall = NBall(dimensions, sphereRadius)

        self.nCube = NCube(dimensions, cubeLength, sampleSize)
        self.nCube.generateUniformSamples()

        norms = self.nCube.generateNorms
        conditions = norms[:] <= sphereRadius
        results = norms[conditions]

        self.volume = len(results) / self.nCube.sampleSize * self.nCube.volume
        return self.volume

    @property
    def difference(self):
        if self.nBall is not None:
            return self.volume - self.nBall.volume
