#This module can be used to automatically calculate burr hole distance, entry point distance, target point distance,
# trajectory angle difference and trajectory length difference within 3D Slicer after appointing fiducials with the following naming convention:

#Fiducial group name: "EVDMarkups_Assessment"
	#Which contains:
	#-"Burrhole_Planned"
	#-"Burrhole_Real"
	#-"Entrypoint_Planned"
	#-"Entrypoint_Real"
	#-"Targetpoint_Planned"
	#-"Targetpoint_Real"

#Planned and real trajectories will be extrapolated from the Burrhole and Entrypoint fiducials.

#Author: J. van Doormaal
#---

# Module for calculating distance between planned and real burr hole
def ShowDistanceBurrhole(unused1=None, unused2=None):
    import math
    markupNodeNames = "EVDMarkups_Assessment"
    markupNode = slicer.util.getFirstNodeByClassByName("vtkMRMLMarkupsFiducialNode", markupNodeNames)

    #Find index of specific labelled fiducials
    burrHolePlannedLabel = "Burrhole_Planned"
    burrHoleRealLabel = "Burrhole_Real"
    global burrHolePlanned
    global burrHoleReal

    for pointIndex in range(markupNode.GetNumberOfControlPoints()):
        label = markupNode.GetNthControlPointLabel(pointIndex)
        if label == burrHolePlannedLabel:
            burrHolePlanned = markupNode.GetNthControlPointPositionWorld(pointIndex)
            print("Coordinates of label", burrHolePlannedLabel, ":", burrHolePlanned)
            break
        else:
            "Burrhole_Planned not found"

    for pointIndex in range(markupNode.GetNumberOfControlPoints()):
        label = markupNode.GetNthControlPointLabel(pointIndex)
        if label == burrHoleRealLabel:
            burrHoleReal = markupNode.GetNthControlPointPositionWorld(pointIndex)
            print("Coordinates of label", burrHoleRealLabel, ":", burrHoleReal)
            break
        else:
            "Burrhole_Real not found"

    burrHoleDistance = math.sqrt((burrHolePlanned[0] - burrHoleReal[0])**2 + (burrHolePlanned[1] - burrHoleReal[1])**2 + (burrHolePlanned[2] - burrHoleReal[2])**2)
    print(f"The distance between the real and planned burr hole is {burrHoleDistance} mm")

# Module for calculating distance between planned and real entry point
def ShowDistanceEntrypoint(unused1=None, unused2=None):
    import math
    markupNodeNames = "EVDMarkups_Assessment"
    markupNode = slicer.util.getFirstNodeByClassByName("vtkMRMLMarkupsFiducialNode", markupNodeNames)

    #Find index and coordinates of specific labelled fiducials
    entrypointPlannedLabel = "Entrypoint_Planned"
    entrypointRealLabel = "Entrypoint_Real"
    global entrypointPlanned
    global entrypointReal

    for pointIndex in range(markupNode.GetNumberOfControlPoints()):
        label = markupNode.GetNthControlPointLabel(pointIndex)
        if label == entrypointPlannedLabel:
            entrypointPlanned = markupNode.GetNthControlPointPositionWorld(pointIndex)
            print("Coordinates of label", entrypointPlannedLabel, ":", entrypointPlanned)
            break
        else:
            "Entrypoint_Planned not found"

    for pointIndex in range(markupNode.GetNumberOfControlPoints()):
        label = markupNode.GetNthControlPointLabel(pointIndex)
        if label == entrypointRealLabel:
            entrypointReal = markupNode.GetNthControlPointPositionWorld(pointIndex)
            print("Coordinates of label", entrypointRealLabel, ":", entrypointReal)
            break
        else:
            "Entrypoint_Real not found"

    # Calculate distance
    entrypointDistance = math.sqrt((entrypointPlanned[0] - entrypointReal[0])**2 + (entrypointPlanned[1] - entrypointReal[1])**2 + (entrypointPlanned[2] - entrypointReal[2])**2)
    print(f"The distance between the real and planned entry point is {entrypointDistance} mm")

# Module for calculating distance between planned and real target point
def ShowDistanceTargetpoint(unused1=None, unused2=None):
    import math
    markupNodeNames = "EVDMarkups_Assessment"
    markupNode = slicer.util.getFirstNodeByClassByName("vtkMRMLMarkupsFiducialNode", markupNodeNames)

    # Find index and coordinates of specific labelled fiducials
    targetpointPlannedLabel = "Targetpoint_Planned"
    targetpointRealLabel = "Targetpoint_Real"
    for pointIndex in range(markupNode.GetNumberOfControlPoints()):
        label = markupNode.GetNthControlPointLabel(pointIndex)
        if label == targetpointPlannedLabel:
            targetpointPlanned = markupNode.GetNthControlPointPositionWorld(pointIndex)
            print("Coordinates of label", targetpointPlannedLabel, ":", targetpointPlanned)
            break
        else:
            "Targetpoint_Planned not found"

    for pointIndex in range(markupNode.GetNumberOfControlPoints()):
        label = markupNode.GetNthControlPointLabel(pointIndex)
        if label == targetpointRealLabel:
            targetpointReal = markupNode.GetNthControlPointPositionWorld(pointIndex)
            print("Coordinates of label", targetpointRealLabel, ":", targetpointReal)
            break
        else:
            "Targetpoint_Real not found"

    targetpointDistance = math.sqrt((targetpointPlanned[0] - targetpointReal[0]) ** 2 + (targetpointPlanned[1] - targetpointReal[1]) ** 2 + (targetpointPlanned[2] - targetpointReal[2]) ** 2)
    print(f"The distance between the real and planned target point is {targetpointDistance} mm")

# Calculate angle and length difference between planned and real EVD trajectory
def ShowAngle(unused1=None, unused2=None):
  import numpy as np

  #Calculate line for EVDTrajectory_Planned
  trajectoryPlannedStartPos = np.array(burrHolePlanned)
  trajectoryPlannedEndPos = np.array(entrypointPlanned)
  trajectoryPlannedDirectionVector = trajectoryPlannedEndPos - trajectoryPlannedStartPos

  # Calculate line for EVDTrajectory_Real
  trajectoryRealStartPos = np.array(burrHoleReal)
  trajectoryRealEndPos = np.array(entrypointReal)
  trajectoryRealDirectionVector = trajectoryRealEndPos - trajectoryRealStartPos

  # Calculate dot product of two vectors
  dotProduct = np.dot(trajectoryPlannedDirectionVector, trajectoryRealDirectionVector)

  # Calculate magnitude per vector
  magnitude_trajectoryPlannedDirectionVector = np.linalg.norm(trajectoryPlannedDirectionVector)
  magnitude_trajectoryRealDirectionVector = np.linalg.norm(trajectoryRealDirectionVector)

  # Calculate the angle in radians using the arccosine of the dot product divided by the product of magnitudes
  trajectoryAngle_radians = np.arccos(dotProduct / (magnitude_trajectoryPlannedDirectionVector * magnitude_trajectoryRealDirectionVector))

  #Convert radians to degrees and display in console
  trajectoryAngle_degrees = np.degrees(trajectoryAngle_radians)
  print(f"The angle between the planned and real trajectory is {trajectoryAngle_degrees} degrees")

  # Calculate length difference between vectors and display in console
  trajectoryLengthDifference = abs(magnitude_trajectoryRealDirectionVector-magnitude_trajectoryPlannedDirectionVector)
  print("Length difference between the vectors is", trajectoryLengthDifference, "mm.")

# Run functions
ShowDistanceBurrhole()
ShowDistanceEntrypoint()
ShowDistanceTargetpoint()
ShowAngle()
