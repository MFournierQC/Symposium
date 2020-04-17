import numpy as np
import matplotlib.pyplot as plt
from MonteCarlo import MonteCarlo


if __name__ == '__main__':
    dimensions = 10
    radius = 1
    length = 2

    iterations = 100
    points = []
    for samples in range(1, 10000):
        mc = MonteCarlo(samples)
        for i in range(iterations):
            volume = mc.nBallVolume(dimensions, length, radius)
            point = (samples, volume)
            points.append(point)

    plt.scatter(points)
    plt.show()
