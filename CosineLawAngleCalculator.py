import math


def calculateAngle(a, b, c):
    """
    Calculate the angle C (in degrees) in a triangle given the lengths of sides a, b, and c.
    a, b, and c are the lengths of the sides of the triangle, with c being the side opposite the angle C.
    """
    # Using the Law of Cosines to calculate the cosine of angle C
    cos_c = (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)

    # Calculating angle C in radians
    angle_c_rad = math.acos(cos_c)

    # Converting the angle from radians to degrees
    angle_c_deg = math.degrees(angle_c_rad)

    return angle_c_deg