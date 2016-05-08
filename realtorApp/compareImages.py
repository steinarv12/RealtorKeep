import math
import operator
from functools import reduce


def computeDiff(image1, image2):
    h1 = image1.histogram()
    h2 = image2.histogram()
    rms = math.sqrt(reduce(operator.add,
                    map(lambda a, b: (a - b)**2, h1, h2)) / len(h1))
    return rms
