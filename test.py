import math


def injectBetweenTwoPoints(startPoint: list, endPoint: list, spacing=1):
    """
    Used in CougarCourse. Adds additional points.
    """

    reverseNessesary = False

    if startPoint[1] < endPoint[1]:
        x1, y1 = startPoint[0], startPoint[1]
        x2, y2 = endPoint[0], endPoint[1]
    elif startPoint[1] > endPoint[1]:
        print("fuck" + str(startPoint) + " -> " + str(endPoint))
        x2, y2 = startPoint[0], startPoint[1]
        x1, y1 = endPoint[0], endPoint[1]
        reverseNessesary = True
    else:
        raise Exception("Start and end point cannot be the same!")

    pointsInBetween = [[x1, y1]]

    totalDistance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    # Calculate spacing.
    numOfPoints = math.ceil(totalDistance / spacing)
    spacing = totalDistance / numOfPoints

    # Angle diff.
    theta = math.atan2((y2 - y1), (x2 - x1))

    for segment in range(numOfPoints):
        newX = math.cos(theta) * spacing + x1
        newY = math.sin(theta) * spacing + y1

        pointsInBetween.append([newX, newY])

        x1 = newX  # Override for next loop.
        y1 = newY  # Override for next loop.

    if reverseNessesary:
        pointsInBetween.reverse()

    return pointsInBetween


def injectPoints(points: list, spacing=2):
    final = []
    for point in points:
        startPoint = [point[0], point[1]]
        endPoint = [point[2], point[3]]

        print(str(startPoint) + " -> " + str(endPoint))

        pointsToInsert = injectBetweenTwoPoints(startPoint, endPoint, spacing)

        for point in pointsToInsert:
            final.append(point)

    return final


def smoothPoints(path: list, weightData=0.999, weightSmooth=0.001, tolerance=0.001):
    """
    Curves a lot of points. Used in
    CougarCourse.
    """
    newPath = path.copy()

    change = tolerance
    while change >= tolerance:
        change = 0
        i = 1
        while i < len(path) - 1:

            j = 0
            while j < len(path[i]):
                aux = newPath[i][j]
                newPath[i][j] += weightData * (
                    path[i][j] - newPath[i][j]
                ) + weightSmooth * (
                    newPath[i - 1][j] + newPath[i + 1][j] - (2 * newPath[i][j])
                )
                change += abs(aux - newPath[i][j])

                j += 1

            i += 1

    return newPath


def assertDistanceAlongCurve(points: list):
    points[0].append(0)
    i = 1
    while i < len(points):
        points[i].append(
            points[i - 1][2]
            + math.sqrt(
                (points[i][0] - points[i - 1][0]) ** 2
                + (points[i][1] - points[i - 1][1]) ** 2
            )
        )
        i += 1

    return points


points = [
    [0, 0, 0, 30],
    [0, 30, -30, 60],
    [-30, 60, -60, 90],
    [-60, 90, -60, 210],
    [-60, 210, -30, 240],
    [-30, 240, 0, 270],
    [0, 270, -30, 300],
    [-30, 300, -60, 270],
    [-60, 270, -30, 240],
    [-30, 240, 0, 210],
    [0, 210, 0, 90],
    [0, 90, -30, 60],
    [-30, 60, -60, 30],
    [-60, 30, -60, 0],
]

newPoints = injectPoints(points)
print("injected " + str(newPoints))

smoothedPoints = assertDistanceAlongCurve(newPoints)
print("\nass " + str(smoothedPoints))