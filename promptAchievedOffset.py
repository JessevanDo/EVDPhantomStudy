def promptAchievedOffset():
    print("Enter achieved offset coordinates in millimeters (x, y, z):")
    x = float(input("X: "))
    y = float(input("Y: "))
    z = float(input("Z: "))
    return [x,y,z]