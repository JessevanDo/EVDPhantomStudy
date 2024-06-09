def pointFinder(point, tri):
    simplex = tri.find_simplex(point)
    return simplex >= 0