import numpy as np
import matplotlib.pyplot as plt
from NDimensionalMonteCarlo import NDimensionalMonteCarlo
from nCube import NCube
from nBall import NBall


if __name__ == '__main__':
    doCompareVolumes = False
    if doCompareVolumes is True:
        dimensions = np.arange(1, 20, 1)
        radius = 1
        length = 2
        cubeVolumes = []
        ballVolumes = []

        for dimension in dimensions:
            nCube = NCube(dimension, length)
            cubeVolumes.append(nCube.volume)

            nBall = NBall(dimension, radius)
            ballVolumes.append(nBall.volume)

        plt.figure(figsize=(8, 8))
        plt.subplot(211)
        plt.scatter(dimensions, ballVolumes, marker='+', s=100, label="Volume d'une n-sphère")
        plt.legend(loc='upper right')
        plt.ylabel(r'Volume $[u^{n}]$')

        plt.subplot(212)
        plt.scatter(dimensions, cubeVolumes, marker='+', s=100, label="Volume d'un n-cube")
        plt.yscale('log')
        plt.xlabel(r'Dimensions $[-]$')
        plt.ylabel(r'Volume $[u^{n}]$')
        plt.legend(loc='upper left')
        plt.show()

    doMC = False
    if doMC is True:
        # Declarations of our useful variables and objects.
        dimensions = 6
        radius = 1
        length = 2
        mc = NDimensionalMonteCarlo(dimensions, radius, length)
        realVolume = mc.nBall.volume

        # Small algorithm for generating the values for our samples.
        iterations = 25
        points = []
        for sampleSize in range(1, 101):
            realSample = sampleSize * 300
            print('Computing Monte Carlo for a sample size of ', realSample)
            for i in range(iterations):
                volume = mc.nBallVolumeUniformSample(realSample)

                point = [realSample, volume]
                points.append(point)

        # Plotting of the values obtained with MC method and comparison to the real value of the volume we seek.
        plt.figure(figsize=(8, 8))
        for point in points:
            plt.scatter(point[0], point[1], s=10)
        plt.plot([1 * 300, 100 * 300], [realVolume, realVolume], 'b--', label='Volume réel = {:.6f}'.format(realVolume))
        plt.axis(xmin=0, xmax=30000)
        ylabel = r'Volume $[u^{%d}]$' % (dimensions)
        plt.ylabel(ylabel)
        plt.xlabel(r"Taille de l'échantillon $[-]$")
        plt.legend(loc='upper right')
        plt.show()

    doLHS = False
    if doLHS is True:
        # Declarations of our useful variables and objects.
        dimensions = 15
        radius = 1
        length = 2
        mc = NDimensionalMonteCarlo(dimensions, radius, length)
        realVolume = mc.nBall.volume

        # Small algorithm for generating the values for our samples.
        iterations = 25
        points = []
        for sampleSize in range(1, 101):
            realSample = sampleSize * 300
            print('Computing Monte Carlo for a sample size of ', realSample)
            for i in range(iterations):
                volume = mc.nBallVolumeLatinHypercubeSample(realSample)

                point = [realSample, volume]
                points.append(point)

        # Plotting of the values obtained with MC method and comparison to the real value of the volume we seek.
        plt.figure(figsize=(8, 8))
        for point in points:
            plt.scatter(point[0], point[1], s=10)
        plt.plot([1 * 300, 100 * 300], [realVolume, realVolume], 'b--', label='Volume réel = {:.6f}'.format(realVolume))
        plt.axis(xmin=0, xmax=30000)
        ylabel = r'Volume $[u^{%d}]$' % (dimensions)
        plt.ylabel(ylabel)
        plt.xlabel(r"Taille de l'échantillon $[-]$")
        plt.legend(loc='upper right')
        plt.show()