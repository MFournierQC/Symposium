import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
from MonteCarlo import MonteCarlo
from nCube import NCube
from nBall import NBall


if __name__ == '__main__':
    dimensions = 5
    radius = 1
    length = 2

    iterations = 20
    points = []
    for sampleSize in range(1, 101):
        mc = MonteCarlo()
        print('Computing Monte Carlo for a sample size of ', sampleSize * 500)
        for i in range(iterations):
            volume = mc.nBallVolume(dimensions, length, radius, sampleSize * 500)
            point = [sampleSize * 500, volume]
            points.append(point)

    for point in points:
        plt.scatter(point[0], point[1], s=10)
    plt.axis(xmin=0, xmax=50000)
    plt.ylabel('Volume')
    plt.xlabel('Sample Size')
    plt.show()
