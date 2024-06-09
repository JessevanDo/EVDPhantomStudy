from scipy.spatial import Delaunay

def createMesh(vertices):
    tri = Delaunay(vertices)
    return tri