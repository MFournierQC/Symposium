import numpy as np
from nBall import NBall
from nCube import NCube


class MonteCarlo:
    def __init__(self, samples):
        self.samples = samples

        self.nBall = None
        self.nCube = None

        self.volume = None

    def nBallVolume(self, dimensions, cubeLength=2, sphereRadius=1):
        self.nBall = NBall(dimensions, sphereRadius)
        self.nCube = NCube(dimensions, cubeLength)
        counter = 0

        for i in range(self.samples):
            randomNorm = self.nCube.randomNorm
            if randomNorm <= self.nBall.r:
                counter += 1

        self.volume = counter / self.samples * self.nCube.volume
        return self.volume

    @property
    def difference(self):
        if self.nBall is not None:
            return self.volume - self.nBall.volume
