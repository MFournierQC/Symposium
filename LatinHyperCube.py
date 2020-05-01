import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import random, sys, os
from copy import deepcopy
import scipy.stats as st


def getIndex(val, h, minVal=0.0, maxVal=1.0):
    minIndex = int(float(minVal / h))
    valIndex = int(float(val / h)) - minIndex

    return valIndex


def indexToEdge(dim, lEdge, h, minVal=0.0, maxVal=1.0):
    rEdge = deepcopy(lEdge)

    for i in range(0, len(lEdge)):
        for j in range(0, dim):
            lEdge[i][j] = getFloatVal(lEdge[i][j], h)
            rEdge[i][j] = lEdge[i][j] + h

    return lEdge, rEdge


def getFloatVal(index, h, minVal=0.0, maxVal=1.0):
    return float(index * h + minVal)


def initializeSpace(dim, numStrata, minVal=0.0, maxVal=1.0, debug='False'):
    dimList = []
    for i in range(0, dim):
        dimList.append(numStrata)

    h = float((maxVal - minVal) / (numStrata))

    return h, getIndex(maxVal, h)


def buildList(dim, numStrata):
    eligibleIndices = []
    iList = []

    for i in range(0, numStrata):
        iList.append(i)

    for i in range(0, dim):
        eligibleIndices.append(iList)

    return eligibleIndices


def getLimitedDraw(dim, eligibleIndices, history):
    # set eligible indices for each dimension

    indices = deepcopy(eligibleIndices)

    for ent in history:
        for i in range(0, dim):
            indices[i] = [x for x in indices[i] if x != ent[i]]

    point = []
    for i in range(0, dim):
        point.append(random.choice(indices[i]))

    return point, indices


def getDraw(dim, eligibleIndices, maxIndex, history):
    eIndex = deepcopy(eligibleIndices)
    point = [0] * dim
    draws = 0
    rejected = 0
    invalid = []
    while True:
        if history == []:
            # Initial random draw
            point = [np.random.randint(0, maxIndex) for x in point]
            history.append(point)
            break
        elif history != []:
            # Limited draw by limiting sample-able indices
            point, eIndex = getLimitedDraw(dim, eIndex, history)
            history.append(point)
            break

    return list(point), history, eIndex


def convertToRandomCDF(dim, history, h):
    # Get bin left edge
    leftEdge = deepcopy(history)
    rightEdge = deepcopy(history)

    # iterate over leftEdge, convert ints to floats

    leftEdge, rightEdge = indexToEdge(dim, leftEdge, h)

    randCDFVal = deepcopy(leftEdge)

    for i in range(0, len(leftEdge)):
        for j in range(0, dim):
            randCDFVal[i][j] = float(np.random.uniform(leftEdge[i][j], 0.999999 * rightEdge[i][j], 1))

    return randCDFVal


def CDFtoNorm(CDF):
    dim = len(CDF[0])
    CDF = deepcopy(CDF)
    for i in range(0, len(CDF)):
        for j in range(0, dim):
            CDF[i][j] = st.norm.ppf(CDF[i][j])
    return CDF


def wtf(data, filename):
    f = open(filename, 'w')
    for ent in data:
        for thing in ent:
            f.write(str(thing) + ',')
        f.write('\n')
    f.close()


def sample(dim, numSamples, ratio):
    numStrata = numSamples

    # Try getting different random points in the array space
    #   to satisfy nearest-neighbor constraint
    # In 3 tries, get another LH sample and go again
    sampleNum = 0
    while True:
        history = []

        h, maxIndex = initializeSpace(dim, numStrata)
        eIndices = buildList(dim, numStrata)
        # Maximum radius within a single cell
        minRadius = h * np.sqrt(dim)

        for i in range(0, numSamples):
            point, history, eIndices = getDraw(dim, eIndices, maxIndex, history)
        sampleNum += 1
        print("Sampling Latin-Hypercube array space (%s)" % (sampleNum))
        tries = 0
        while True:
            randUniform = convertToRandomCDF(dim, history, h)
            randStandardNorm = CDFtoNorm(randUniform)
            tries += 1

            wtf(randUniform, 'utemp.csv')
            wtf(randStandardNorm, 'ntemp.csv')

            cols = range(0, dim)
            randUniform = np.genfromtxt('utemp.csv', delimiter=',', usecols=cols)
            randStandardNorm = np.genfromtxt('ntemp.csv', delimiter=',', usecols=cols)

            uninnd = nnd(randUniform)
            normnnd = nnd(randStandardNorm)
            sampleMin = np.nanmin(uninnd)
            sampleMinNorm = np.nanmin(normnnd)
            print(sampleMin, sampleMinNorm, ratio * minRadius)

            if tries == 3:
                break
            if sampleMin > ratio * minRadius and sampleMinNorm > ratio * minRadius:
                break
        if sampleMin > ratio * minRadius and sampleMinNorm > ratio * minRadius:
            break

    os.remove(os.getcwd() + '/utemp.csv')
    os.remove(os.getcwd() + '/ntemp.csv')

    return randUniform, randStandardNorm


def nnd(a):
    # For each sample, get the nearest neighbor w.r.t. each variable
    b = np.zeros((a.shape[0], a.shape[0]), dtype=float)
    for i in range(0, b.shape[0]):
        for j in range(0, b.shape[0]):
            b[i, j] = radius(a[j, :] - a[i, :])
            if i == j:
                b[i, j] = 10e3
    return b


def radius(v):
    a = np.nansum(v * v)
    return np.sqrt(a)


if __name__ == "__main__":
    dim = 3
    numSamples = 50
    minRatio = 1.0

    # Get standard normal and standard uniform samples
    uni, std = sample(dim, numSamples, minRatio)

    if dim == 2:
        h = 1.0 / numSamples
        for i in range(1, numSamples):
            plt.plot((0, 1), (i * h, i * h), 'k--', linewidth=1)
            plt.plot((i * h, i * h), (0, 1), 'k--', linewidth=1)

        plt.plot(uni[:, 0], uni[:, 1], 'ro')
        plt.xlabel('X', fontsize=18)
        plt.ylabel('Y', fontsize=18)
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.show()

    if dim == 3:
        h = 1.0 / numSamples
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(uni[:, 0], uni[:, 2], uni[:, 2], 'ro')
        ax.plot(std[:, 0], std[:, 2], std[:, 2], 'bo')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()