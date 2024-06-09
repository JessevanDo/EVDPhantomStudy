import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import trimesh
from trimesh import Trimesh
from Scripts.readTargetPoint import readTargetPoint
from Scripts.selectFile import selectFile
from Scripts.drainSpatialCalculator import drainSpatialCalculator
from Scripts.calculateIntersection import calculateIntersection
from mpl_toolkits.mplot3d import Axes3D
from Scripts.pointFinder import pointFinder
from loadSTL import loadSTL
from createMesh import createMesh
from stl import mesh
from Scripts.plotVentricles import plotVentricles
from Scripts.simplifyMesh import simplifyMesh

def main():

    # Select file path of ventricles .stl
    print("Select the .stl file representing the ventricles segmentation:")
    filePath = selectFile()

    # Load STL file
    print("Loading STL file...")
    ventricularMesh = trimesh.load(filePath)

    # Calculate volume of raw mesh
    volume = ventricularMesh.volume
    print(f"Calculated volume of mesh is: {volume} mm3")

    # Simplify Mesh
    print("Simplifying Mesh...")
    vertices, faces = simplifyMesh(filePath)

    # Create simplified mesh for visualization
    simplifiedVentricularMesh = createMesh(vertices)

    # Run drainSpatialCalculator to determine relevant points:
    print("Calculating relative positions...")
    (drain, target, burr, distanceTrajectory, distanceDrain, distanceToTarget, angularError) = drainSpatialCalculator()

    # Calculate whether drain tip is inside mesh
    inside = pointFinder(drain, simplifiedVentricularMesh)
    if inside == True:
        print("The achieved drain position is inside the ventricles.")
    else:
        print("The achieved drain position is outside the ventricles.")

    # Calculate intersection point for drain
    intersectionPointDrain = calculateIntersection("Drain", ventricularMesh, burr, drain)

    # Calculate intersection point for ideal trajectory
    intersectionPointTrajectory = calculateIntersection("Trajectory", ventricularMesh, burr, target)

    # Run 3D plotting function
    print("Creating 3D plot...")
    plotVentricles(vertices, target, drain, burr, intersectionPointDrain, intersectionPointTrajectory, inside, faces)

# Run main function and print result
main()
print("Script execution complete.")


