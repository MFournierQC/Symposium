import numpy as np
import matplotlib.pyplot as plt
from NDimensionalMonteCarlo import NDimensionalMonteCarlo
from nCube import NCube
from nBall import NBall


if __name__ == '__main__':
    radius = 1
    length = 2

    doCompareVolumes = False
    if doCompareVolumes is True:
        dimensions = np.arange(1, 20, 1)
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
        dimensions = 2
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

                resultingVector = [realSample, volume]
                points.append(resultingVector)

        # Plotting of the values obtained with MC method and comparison to the real value of the volume we seek.
        plt.figure(figsize=(8, 8))
        for resultingVector in points:
            plt.scatter(resultingVector[0], resultingVector[1], s=10)
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
        dimensions = 6
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

                resultingVector = [realSample, volume]
                points.append(resultingVector)

        # Plotting of the values obtained with MC method and comparison to the real value of the volume we seek.
        plt.figure(figsize=(8, 8))
        for resultingVector in points:
            plt.scatter(resultingVector[0], resultingVector[1], s=10)
        plt.plot([1 * 300, 100 * 300], [realVolume, realVolume], 'b--', label='Volume réel = {:.6f}'.format(realVolume))
        plt.axis(xmin=0, xmax=30000)
        ylabel = r'Volume $[u^{%d}]$' % (dimensions)
        plt.ylabel(ylabel)
        plt.xlabel(r"Taille de l'échantillon $[-]$")
        plt.legend(loc='upper right')
        plt.show()

    doCompareConvergence = False
    if doCompareConvergence is True:
        # Declarations of our useful variables and objects.
        dimensions = 2
        mc = NDimensionalMonteCarlo(dimensions, radius, length)
        realVolume = mc.nBall.volume
        sampleSizes = np.arange(300, 30300, 300)
        mcDifferences = []
        lhsDifferences = []

        # Small algorithm for generating the values for our samples.
        iterations = 25
        for sampleSize in sampleSizes:
            print('Computing Monte Carlo for a sample size of ', sampleSize)
            mcDifferences.append(0)
            lhsDifferences.append(0)

            i = int((sampleSize / 300) - 1)

            for iter in range(iterations):
                mcVolume = mc.nBallVolumeUniformSample(sampleSize)
                if mc.difference > mcDifferences[i]:
                    mcDifferences[i] = mc.difference

                lhsVolume = mc.nBallVolumeLatinHypercubeSample(sampleSize)
                if mc.difference > lhsDifferences[i]:
                    lhsDifferences[i] = mc.difference

        # Plotting of the values obtained with MC method and comparison to the real value of the volume we seek.
        plt.figure(figsize=(8, 4))
        plt.plot(sampleSizes, mcDifferences, c='red', label='Monte Carlo')
        plt.plot(sampleSizes, lhsDifferences, c='black', label='LHS')
        plt.axis(xmin=0, xmax=30000)
        ylabel = r'$\Delta V_{max}$ $[u^{%d}]$' % (dimensions)
        plt.ylabel(ylabel)
        plt.xlabel(r"Taille de l'échantillon $[-]$")
        plt.legend(loc='upper right')
        plt.show()

    doVisualizeSampling = False
    if doVisualizeSampling is True:
        dimensions = 2
        nCube = NCube(dimensions, length)

        nCube.uniformSample(10)
        mcPoints = nCube.samples
        nCube.uniformLatinHypercubeSample(10)
        lhsPoints = nCube.samples
        plt.figure(figsize=(8, 8))
        plt.subplot(221)
        plt.gca().set_title(r'($\mathbf{a}$) 10 points')
        plt.scatter(mcPoints[:, 0], mcPoints[:, 1], c='red', marker='+', s=70)
        plt.scatter(lhsPoints[:, 0], lhsPoints[:, 1], c='black', marker='x')
        plt.axis(xmin=-1, xmax=1, ymin=-1, ymax=1)

        nCube.uniformSample(20)
        mcPoints = nCube.samples
        nCube.uniformLatinHypercubeSample(20)
        lhsPoints = nCube.samples
        plt.subplot(222)
        plt.gca().set_title(r'($\mathbf{b}$) 20 points')
        plt.scatter(mcPoints[:, 0], mcPoints[:, 1], c='red', label='MC', marker='+', s=70)
        plt.scatter(lhsPoints[:, 0], lhsPoints[:, 1], c='black', label='LHS', marker='x')
        plt.legend(loc='upper right')
        plt.axis(xmin=-1, xmax=1, ymin=-1, ymax=1)

        nCube.uniformSample(50)
        mcPoints = nCube.samples
        nCube.uniformLatinHypercubeSample(50)
        lhsPoints = nCube.samples
        plt.subplot(223)
        plt.gca().set_title(r'($\mathbf{c}$) 50 points')
        plt.scatter(mcPoints[:, 0], mcPoints[:, 1], c='red', marker='+', s=70)
        plt.scatter(lhsPoints[:, 0], lhsPoints[:, 1], c='black', marker='x')
        plt.xlabel(r'Position en $x_{1}$ $[u]$')
        plt.ylabel(r'Position en $x_{2}$ $[u]$')
        plt.axis(xmin=-1, xmax=1, ymin=-1, ymax=1)

        nCube.uniformSample(100)
        mcPoints = nCube.samples
        nCube.uniformLatinHypercubeSample(100)
        lhsPoints = nCube.samples
        plt.subplot(224)
        plt.gca().set_title(r'($\mathbf{d}$) 100 points')
        plt.scatter(mcPoints[:, 0], mcPoints[:, 1], c='red', marker='+', s=70)
        plt.scatter(lhsPoints[:, 0], lhsPoints[:, 1], c='black', marker='x')
        plt.axis(xmin=-1, xmax=1, ymin=-1, ymax=1)

        plt.show()

    doCompareUniformity = False
    if doCompareUniformity is True:
        dimensions = 3
        nCube = NCube(dimensions, length)
        sampleSizes = np.arange(300, 30300, 300)

        mcResults = []
        lhsResults = []

        for iter in [1, 2, 3]:
            mcIterNorms = []
            lhsIterNorms = []
            for sampleSize in sampleSizes:
                nCube.uniformSample(sampleSize)
                mcPoints = nCube.samples
                resultingVector = [np.sum(mcPoints[:, 0]), np.sum(mcPoints[:, 1]), np.sum(mcPoints[:, 2])]
                mcIterNorms.append(np.linalg.norm(resultingVector))

                nCube.uniformLatinHypercubeSample(sampleSize)
                lhsPoints = nCube.samples
                resultingVector = [np.sum(lhsPoints[:, 0]), np.sum(lhsPoints[:, 1]), np.sum(lhsPoints[:, 2])]
                lhsIterNorms.append(np.linalg.norm(resultingVector))

            mcResults.append(mcIterNorms)
            lhsResults.append(lhsIterNorms)

        plt.figure(figsize=(8, 8))
        plt.subplot(211)
        plt.gca().set_title(r'($\mathbf{a}$) Monte Carlo')
        plt.plot(sampleSizes, mcResults[0], color='#ff0000', label='Itération 1', linewidth='2')
        plt.plot(sampleSizes, mcResults[1], color='#ff6600', label='Itération 2', linewidth='2')
        plt.plot(sampleSizes, mcResults[2], color='#ffaa00', label='Itération 3', linewidth='2')
        plt.legend(loc='upper left')

        plt.subplot(212)
        plt.gca().set_title(r'($\mathbf{b}$) Hypercube Latin')
        plt.plot(sampleSizes, lhsResults[0], color='#000000', label='Itération 1', linewidth='2')
        plt.plot(sampleSizes, lhsResults[1], color='#666666', label='Itération 2', linewidth='2')
        plt.plot(sampleSizes, lhsResults[2], color='#aaaaaa', label='Itération 3', linewidth='2')
        plt.xlabel(r"Taille de l'échantillon $[-]$")
        plt.ylabel(r'Norme du vecteur résultant $[u]$')
        plt.legend(loc='upper right')
        plt.show()

