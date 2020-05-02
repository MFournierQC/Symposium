from nBall import NBall
from nCube import NCube


class NDimensionalMonteCarlo:
    def __init__(self, dimensions, radius=1, length=2):
        self.dimensions = dimensions
        self.nBall = NBall(dimensions, radius)
        self.nCube = NCube(dimensions, length)
        self.volume = None

    def checkConditions(self, norms):
        conditions = norms[:] <= self.nBall.r
        return norms[conditions]

    def nBallVolumeUniformSample(self, sampleSize=10000):
        self.nCube.uniformSample(sampleSize)
        norms = self.nCube.generateNorms
        results = self.checkConditions(norms)

        self.volume = (len(results) / sampleSize) * self.nCube.volume
        return self.volume

    def nBallVolumeLatinHypercubeSample(self, sampleSize=10000):
        self.nCube.uniformLatinHypercubeSample(sampleSize)
        norms = self.nCube.generateNorms
        results = self.checkConditions(norms)

        self.volume = (len(results) / sampleSize) * self.nCube.volume
        return self.volume

    @property
    def difference(self):
        return abs(self.volume - self.nBall.volume)
