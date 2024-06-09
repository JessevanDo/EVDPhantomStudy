import math
from Scripts.CosineLawAngleCalculator import calculateAngle
from Scripts.EuclidianDistanceCalculator import distance

def drainSpatialCalculator():
    # Prompt the user to input the coordinates of the target point:
    xTarget = float(input("Enter the x-coordinate of the target point: "))
    yTarget = float(input("Enter the y-coordinate of the target point: "))
    zTarget = float(input("Enter the z-coordinate of the target point: "))
    target = (xTarget, yTarget, zTarget)

    # Prompt the user to input the coordinates of the burr hole:
    xBurr = float(input("Enter the x-coordinate of the Burr hole (most inferior part of Burr midline): "))
    yBurr = float(input("Enter the y-coordinate of the Burr hole (most inferior part of Burr midline): "))
    zBurr = float(input("Enter the z-coordinate of the Burr hole (most inferior part of Burr midline): "))
    burr = (xBurr, yBurr, zBurr)

    # Ask whether stereotactic frame is necessary:
    stereotacticPresent = input("Is correction for a stereotactic frame necessary? (True/False)")

    # Enter loop for stereotactic frame:
    if stereotacticPresent == "True":
        # Prompt the user to input the coordinates of the stereotactic frame:
        xStereotactic = float(input("Enter the 3D Slicer x-coordinate of the origin point of the stereotactic frame:"))
        yStereotactic = float(input("Enter the 3D Slicer x-coordinate of the origin point of the stereotactic frame:"))
        zStereotactic = float(input("Enter the 3D Slicer z-coordinate of the origin point fo the stereotactic frame:"))

        # Prompt the user to input the coordinates of the drain tip measured by the stereotactic frame:
        xDrain = float(input("Enter the x-coordinate of the drain tip, measured by the stereotactic frame:"))
        yDrain = float(input("Enter the y-coordinate of the drain tip, measured by the stereotactic frame:"))
        zDrain = float(input("Enter the z-coordinate of the drain tip, measured by the stereotactic frame:"))

        # Normalize for stereotactic frame:
        drain = (xDrain + xStereotactic, yDrain + yStereotactic, zDrain + zStereotactic)
        print(f"Normalized coordinates of drain tip are: {drain}")

    else:
        # Prompt the user to input the coordinates of the drain tip measured in 3D Slicer:
        xDrain = float(input("Enter the x-coordinate of the drain tip:"))
        yDrain = float(input("Enter the y-coordinate of the drain tip:"))
        zDrain = float(input("Enter the z-coordinate of the drain tip:"))
        drain = (xDrain, yDrain, zDrain)

    # Calculate the distances between the points
    distanceTrajectory =distance(target, burr)
    distanceDrain = distance(drain, burr)
    distanceToTarget = distance(target, drain)

    # Print the distances
    print(f"The trajectory length is: {distanceTrajectory:.2f}")
    print(f"The drain length is: {distanceDrain:.2f}")
    print(f"The distance to target is: {distanceToTarget:.2f}")

    # Calculate and print angular error
    angularError = calculateAngle(distanceTrajectory, distanceDrain, distanceToTarget)
    print(f"The angular inaccuracy is: {angularError} degrees.")

    return (drain, target, burr, distanceTrajectory, distanceDrain, distanceToTarget, angularError)