import math


def pointDistance(keyPoint):
    """
    :param keyPoint:
    :return:list
    :distance:
    """
    distance0 = (keyPoint[4][0] - keyPoint[9][0]) ** 2 + (keyPoint[4][1] - keyPoint[9][1]) ** 2
    distance1 = (keyPoint[7][0] - keyPoint[12][0]) ** 2 + (keyPoint[7][1] - keyPoint[12][1]) ** 2
    distance2 = (keyPoint[2][0] - keyPoint[4][0]) ** 2 + (keyPoint[2][1] - keyPoint[4][1]) ** 2
    distance3 = (keyPoint[5][0] - keyPoint[7][0]) ** 2 + (keyPoint[5][1] - keyPoint[7][1]) ** 2
    distance4 = (keyPoint[0][0] - keyPoint[4][0]) ** 2 + (keyPoint[0][1] - keyPoint[4][1]) ** 2
    distance5 = (keyPoint[0][0] - keyPoint[7][0]) ** 2 + (keyPoint[0][1] - keyPoint[7][1]) ** 2
    distance6 = (keyPoint[4][0] - keyPoint[10][0]) ** 2 + (keyPoint[4][1] - keyPoint[10][1]) ** 2
    distance7 = (keyPoint[7][0] - keyPoint[13][0]) ** 2 + (keyPoint[7][1] - keyPoint[13][1]) ** 2
    distance8 = (keyPoint[4][0] - keyPoint[7][0]) ** 2 + (keyPoint[4][1] - keyPoint[7][1]) ** 2
    distance9 = (keyPoint[11][0] - keyPoint[14][0]) ** 2 + (keyPoint[11][1] - keyPoint[14][1]) ** 2
    distance10 = (keyPoint[10][0] - keyPoint[13][0]) ** 2 + (keyPoint[10][1] - keyPoint[13][1]) ** 2
    distance11 = (keyPoint[6][0] - keyPoint[10][0]) ** 2 + (keyPoint[6][1] - keyPoint[10][1]) ** 2
    distance12 = (keyPoint[3][0] - keyPoint[13][0]) ** 2 + (keyPoint[3][1] - keyPoint[13][1]) ** 2
    distance13 = (keyPoint[4][0] - keyPoint[23][0]) ** 2 + (keyPoint[4][1] - keyPoint[23][1]) ** 2
    distance14 = (keyPoint[7][0] - keyPoint[20][0]) ** 2 + (keyPoint[7][1] - keyPoint[20][1]) ** 2

    return [distance0, distance1, distance2, distance3, distance4, distance5, distance6, distance7,
            distance8, distance9, distance10, distance11, distance12, distance13, distance14]


def pointAngle(keyPoint):
    angle0 = __myAngle(keyPoint[2], keyPoint[3], keyPoint[4])
    angle1 = __myAngle(keyPoint[5], keyPoint[6], keyPoint[7])
    angle2 = __myAngle(keyPoint[9], keyPoint[10], keyPoint[11])
    angle3 = __myAngle(keyPoint[12], keyPoint[13], keyPoint[14])
    angle4 = __myAngle(keyPoint[3], keyPoint[2], keyPoint[1])
    angle5 = __myAngle(keyPoint[6], keyPoint[5], keyPoint[1])
    angle6 = __myAngle(keyPoint[10], keyPoint[8], keyPoint[13])
    angle7 = __myAngle(keyPoint[7], keyPoint[12], keyPoint[13])
    angle8 = __myAngle(keyPoint[4], keyPoint[9], keyPoint[10])
    angle9 = __myAngle(keyPoint[4], keyPoint[0], keyPoint[7])
    angle10 = __myAngle(keyPoint[4], keyPoint[8], keyPoint[7])
    angle11 = __myAngle(keyPoint[1], keyPoint[8], keyPoint[13])
    angle12 = __myAngle(keyPoint[1], keyPoint[8], keyPoint[10])
    angle13 = __myAngle(keyPoint[4], keyPoint[1], keyPoint[8])
    angle14 = __myAngle(keyPoint[7], keyPoint[1], keyPoint[8])

    return [angle0, angle1, angle2, angle3, angle4, angle5, angle6, angle7,
            angle8, angle9, angle10, angle11, angle12, angle13, angle14]


def __myAngle(A, B, C):
    c = math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)
    a = math.sqrt((B[0] - C[0]) ** 2 + (B[1] - C[1]) ** 2)
    b = math.sqrt((A[0] - C[0]) ** 2 + (A[1] - C[1]) ** 2)
    if 2 * a * c != 0:
        return (a ** 2 + c ** 2 - b ** 2) / (2 * a * c)
    return 0
