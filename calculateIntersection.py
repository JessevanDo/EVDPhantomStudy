import trimesh
import numpy as np

def calculateIntersection(lineName, mesh, lineStart, lineEnd):

    manualInput = input(f"Do you want to manually input the intersection point for the {lineName}? If you select 'False', intersection point will be extrapolated from start and beginning of line. (True/False):")
    """
    Find the intersection between a mesh and a line.
    If there are multiple intersections, return the one with the highest z-coordinate.

    Args:
    - mesh (trimesh.Trimesh): The mesh object to intersect.
    - line_start (array-like): The starting point of the line (x, y, z).
    - line_end (array-like): The ending point of the line (x, y, z).

    Returns:
    - intersection_point (np.array): The intersection point with the highest z-coordinate.
      Returns None if no intersection is found.
    """

    if manualInput == True:
        xIntersection = input("Input x coordinate of intersection point:")
        yIntersection = input("Input y coordinate of intersection point:")
        zIntersection = input("Input z coordinate of intersection point:")
        intersection = (xIntersection, yIntersection, zIntersection)

    else:
        rayOrigin = np.array(lineStart)
        rayDirection = np.array(lineEnd) - np.array(lineStart)
        rayDirection = rayDirection / np.linalg.norm(rayDirection)  # Normalize the direction vector

        # Perform the ray-mesh intersection
        locations, indexRay, indexTri = mesh.ray.intersects_location([rayOrigin], [rayDirection])

        if len(locations) == 0:
            # No intersection
            return None

        # Find the intersection with the highest z-coordinate
        intersection = locations[np.argmax(locations[:, 2])]

    return intersection
