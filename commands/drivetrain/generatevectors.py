import os, math

import robot


def assertDistanceAlongCurve(points: list):
    points[0].append(0)
    i = 1
    while i < len(points):
        points[i].append(
            points[i - 1][3]
            + math.sqrt(
                (points[i][0] - points[i - 1][0]) ** 2
                + (points[i][1] - points[i - 1][1]) ** 2
            )
        )
        i += 1

    return points


class GenerateVectors:
    @staticmethod
    def generate(file="Unnamed.wpilib.json"):

        with open(os.path.dirname(robot.__file__) + "/" + file) as f:
            json = f.read()

        l = eval(json)

        valuableData = []

        count = 10

        for data in l:

            if count == 10:

                valuableData.append(
                    [
                        data["pose"]["translation"]["x"]
                        * 39.3701,  # This is the order we need
                        data["pose"]["translation"]["y"] * 39.3701,
                        data["velocity"],
                    ]
                )

                count = 0

            count += 1

        return assertDistanceAlongCurve(valuableData)
