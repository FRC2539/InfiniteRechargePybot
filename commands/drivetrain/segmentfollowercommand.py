from commands2 import CommandBase

import math

import robot


class SegmentFollowerCommand(CommandBase):
    def __init__(self, waypoints: list, angleTolerance=5):
        """
        You start at [0, 0].
        """
        super().__init__()

        waypoints.insert(0, [0, 0])  # Adds the first point.

        self.addRequirements(robot.drivetrain)

        self.tol = angleTolerance

        self.distances = []
        self.angles = []

        for i in range(len(waypoints)):
            try:
                point, nextPoint = (
                    waypoints[i],
                    waypoints[i + 1],
                )  # Get two consecutive points.
            except (IndexError):
                break

            # Get each point's components.
            pointX, nextPointX = point[0], nextPoint[0]
            pointY, nextPointY = point[1], nextPoint[1]

            # Find the difference between them.
            finalX = nextPointX - pointX
            finalY = nextPointY - pointY

            if finalX == 0 and finalY == 0:  # Same points, continue onto the next pair.
                continue

            if finalX == 0:
                if nextPointY > pointY:
                    theta = 0
                else:
                    theta = 180

            elif finalY == 0:
                if nextPointX > pointX:
                    theta = 90
                else:
                    theta = -90

            else:
                theta = math.atan2(finalX, finalY) * 180 / math.pi

            distance = math.sqrt(finalX ** 2 + finalY ** 2)

            self.distances.append(distance)
            self.angles.append(theta)

    def initialize(self):
        robot.drivetrain.setModuleProfiles(0, drive=False)

        self.pointTracker = 1
        self.totalPathsCompleted = 0

        self.startPos = robot.drivetrain.getPositions()

        self.desiredAngle = self.angles[0]
        self.desiredDistance = self.distances[0]

        self.firstPoint = (
            True  # A cheat to sneak past the atWaypoint for the first point.
        )
        self.notRanYet = True
        self.moveSet = False

        print(self.distances)
        print(self.angles)

    def execute(self):

        if self.atWaypoint() or self.firstPoint:

            if self.notRanYet:  # Runs once at the waypoint.
                robot.drivetrain.stop()

                self.startPos = robot.drivetrain.getPositions()

                self.desiredAngle = self.angles[self.pointTracker]
                self.desiredDistance = self.distances[self.pointTracker]

                robot.drivetrain.setUniformModuleAngle(self.desiredAngle)

                self.notRanYet = False

                self.pointTracker += 1

            self.count = 0
            if self.count != 4 and not self.moveSet:
                for currentAngle in robot.drivetrain.getModuleAngles():
                    if (
                        abs(currentAngle - self.desiredAngle) < self.tol
                        or abs(currentAngle - self.desiredAngle - 360) < self.tol
                    ):
                        self.count += 1
                    else:
                        continue

            if self.count == 4:  # All angles aligned.
                robot.drivetrain.setUniformModulePosition(self.desiredDistance)

                self.moveSet = True

        else:
            self.moveSet = False
            self.notRanYet = True
            self.firstPoint = False

    def atWaypoint(self):
        count = 0
        for position, start in zip(robot.drivetrain.getPositions(), self.startPos):
            if (
                abs(position - (start + self.desiredDistance)) < 4
            ):  # 4 inches is the tolerance.
                count += 1
            else:
                return False

        if count == 4:
            self.totalPathsCompleted += 1
            return True

    def isFinished(self):
        return self.totalPathsCompleted == (len(self.distances) - 1)

    def end(self, interrupted):
        robot.drivetrain.stop()
