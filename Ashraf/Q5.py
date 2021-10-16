import numpy


def Q5():
    mat = numpy.zeros(shape=(4, 4))
    for i in range(4):
        mat[i, i] = i + 1

    return mat
