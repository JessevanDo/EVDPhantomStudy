import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

def plotVentricles(vertices, target, drain, burr, intersectionDrain, intersectionTrajectory, inside, faces):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Ensure face arrays indices are within bounds of vertices indices
    maxIndex = len(vertices) - 1
    validFaces = np.all(faces <= maxIndex, axis=1)
    faces = faces[validFaces]

    # Create a Poly3DCollection
    mesh = Poly3DCollection(vertices[faces], alpha=0.1, linewidths=0.1, edgecolors='b')
    mesh.set_facecolor((0.5, 0.5, 1, 0.3))
    ax.add_collection3d(mesh)

    # Plot target point
    ax.scatter(target[0], target[1], target[2], color='g', s=20, label='Target Point')

    # Plot drain tip
    color = 'r' if inside else 'y'
    ax.scatter(drain[0], drain[1], drain[2], color=color, s=20, label='Achieved Position')

    # Plot burr hole
    ax.scatter(burr[0], burr[1], burr[2], color='y', s=20, label='Burr hole')

    # Plot drain intersection point
    ax.scatter(intersectionDrain[0], intersectionDrain[1], intersectionDrain[2], color='m', s=20, label='Intersection Point Drain')

    # Plot trajectory intersection point
    ax.scatter(intersectionTrajectory[0], intersectionTrajectory[1], intersectionTrajectory[2], color='m', s=20, label='Intersection Point Ideal Trajectory')

    # Plot line between burr and drain intersection
    ax.plot([burr[0], intersectionDrain[0]], [burr[1], intersectionDrain[1]], [burr[2], intersectionDrain[2]], color='y', linestyle='-', linewidth=1, label='Achieved Trajectory until intersection')

    # Plot line between drain intersection and drain tip
    ax.plot([intersectionDrain[0], drain[0]], [intersectionDrain[1], drain[1]], [intersectionDrain[2], drain[2]], color='y', linestyle='-', linewidth=1, label='Achieved Trajectory after intersection')

    # Plot line between burr and ideal intersection
    ax.plot([burr[0], intersectionTrajectory[0]], [burr[1], intersectionTrajectory[1]], [burr[2], intersectionTrajectory[2]], color='k', linestyle='-', linewidth=1, label='Ideal Trajectory until intersection')

    # Plot line between ideal intersection and target
    ax.plot([intersectionTrajectory[0], target[0]], [intersectionTrajectory[1], target[1]], [intersectionTrajectory[2], target[2]], color='k', linestyle='-', linewidth=1, label='Ideal Trajectory after intersection')

    # Labels and legend
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    ax.set_title('3D Visualization of Ventricles and Drain Positions')

    # Set limits
    ax.set_xlim(np.min(vertices[:, 0]), np.max(vertices[:, 0]))
    ax.set_ylim(np.min(vertices[:, 1]), np.max(vertices[:, 1]))
    ax.set_zlim(np.min(vertices[:, 2]), np.max(vertices[:, 2]))

    plt.show()