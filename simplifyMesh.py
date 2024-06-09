from pyntcloud import PyntCloud
import pandas as pd
import trimesh

def simplifyMesh(filePath, targetReduction=0.1):
    ventricularMesh = trimesh.load(filePath)

    simplifiedMesh = ventricularMesh.simplify_quadratic_decimation(int(len(ventricularMesh.vertices)* targetReduction))

    return simplifiedMesh.vertices, simplifiedMesh.faces