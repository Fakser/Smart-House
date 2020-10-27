from Clustering.controller import math, sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Clustering.utils import is_iter


def geometric_distance(a, b, dist = 0):
    """ 
    Loss function calculating geometric distance between 2 objects.
    It can be explained by the example of distance between two points
    on 2D plane.

     ^
     |        .B(x2, y2)
     |       /
     |      /
     |     .A(x1, y1)
     |
     + --------------------- >
                   
    It is derived by:
    sqrt((x1 - x2)^2 + (y1 - y2)^2)
    This implementation of distance metric is multidimensional, which enables
    calculation of geometric distance between 

    Args:
        a (object): first object
        b (object): second object of same length as object a
        dist (int, optional): [description]. Defaults to 0.

    Returns:
        float: value of geometric distance 
    """
    if is_iter(a) and is_iter(b) and len(a) == len(b):
        if is_iter(a[0]) == False: 
            dist += math.sqrt(sum([math.pow(float(a[i]) - float(b[i]), 2) for i in range(len(a))]))
        else:
            for index in range(len(a)):
                dist += geometric_distance(a[index], b[index], dist)
    elif is_iter(a) == False and is_iter(b) == False:
        dist += abs(a - b)
    return dist


