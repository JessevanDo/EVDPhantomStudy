import math

def distance(point1, point2):
    """
    Calculate the Euclidean distance between two points in 3D space.
    Each point is represented as a tuple (x, y, z).
    """
    return math.sqrt((point1[0] - point2[0])**2 +
                     (point1[1] - point2[1])**2 +
                     (point1[2] - point2[2])**2)