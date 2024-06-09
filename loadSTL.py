from stl import mesh

def loadSTL(filePath):
    ventricleMesh = mesh.Mesh.from_file(filePath)
    return ventricleMesh

