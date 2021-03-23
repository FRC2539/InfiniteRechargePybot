from commands2 import CommandBase

import math

import robot


class SegmentFollowerCommand(CommandBase):
    def __init__(
        self,
        waypoints: list,
        angleTolerance=5,
        maxSpeed=1,
        deccelerate=False,
        speedOffset=0,
        kP=0.0325,
        startingAngle=None,
        stopWhenDone=True,
    ):
        """
        You start at [0, 0]. speedOffset is applied
        to the left hand side of the drivetrain! Note,
        this is not exactly accurate, but it is pretty consistent!
        If you don't wanna correct the heading, leave kP as 0. If
        you want to correct it relative to zero (instead of the captured
        starting angle) leave startingAngle as None.s
        """
        super().__init__()

        waypoints.insert(0, [0, 0])  # Adds the first point.

        self.addRequirements(robot.drivetrain)

        self.tol = angleTolerance
        self.deccelerate = deccelerate
        self.speedOffset = speedOffset
        self.kP = kP
        self.startingAngle = startingAngle
        self.stopWhenDone = stopWhenDone

        self.maxSpeed = maxSpeed

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
                    theta = 180
                else:
                    theta = 0

            elif finalY == 0:
                if nextPointX > pointX:
                    theta = 90
                else:
                    theta = -90

            else:
                if finalX > 0:  # Going to the right
                    theta = ((math.atan2(finalY, finalX) * 180 / math.pi) + 90) % 180
                else:  # Going to the left
                    theta = -((math.atan2(finalX, finalY) * 180 / math.pi) % 180)

            distance = math.sqrt(finalX ** 2 + finalY ** 2)

            self.distances.append(distance)
            self.angles.append(theta)

        print("d " + str(self.distances))
        print("a " + str(self.angles))

    def initialize(self):
        robot.drivetrain.setModuleProfiles(1, turn=False)

        self.pointTracker = 0

        if self.startingAngle is None:
            self.startingAngle = 0
        else:
            self.startingAngle = robot.drivetrain.getAngle()

        self.startPos = robot.drivetrain.getPositions()

        self.desiredAngle = self.angles[0]
        self.desiredDistance = self.distances[0]

        self.lastDisplacement = self.desiredDistance

        self.pathFinished = False
        self.notRanYet = True
        self.moveSet = False
        self.passed = True

    def execute(self):

        robot.drivetrain.setUniformModuleAngle(self.desiredAngle)

        if self.atWaypoint():  # Watches to see if we pass the desired waypoint.
            self.startPos = robot.drivetrain.getPositions()
            self.passed = True

        if self.passed:  # Have we gone through the waypoint?

            if self.notRanYet:  # Runs once at the waypoint.

                try:  # If it can't index them, then it's done.
                    self.desiredAngle = self.angles[self.pointTracker]
                    self.desiredDistance = self.distances[self.pointTracker]

                    self.lastDisplacement = self.desiredDistance

                except (IndexError):
                    self.pathFinished = True
                    return

                self.pointTracker += 1

                self.notRanYet = False

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

            if self.count >= 2:  # All angles aligned.
                # Add extra speed because the robot can't follow a damn straight line. My need Weaver's heading
                # algo.
                robot.drivetrain.setSpeeds(
                    [
                        self.maxSpeed + self.speedOffset,
                        self.maxSpeed,
                        self.maxSpeed + self.speedOffset,
                        self.maxSpeed,
                    ]
                )
                self.moveSet = True
                self.passed = False

        else:
            self.moveSet = False
            self.notRanYet = True

            speedOffset = robot.drivetrain.getAngleTo(self.startingAngle) * self.kP

            print("so " + str(speedOffset))

            if self.deccelerate:
                if (
                    abs(
                        self.desiredDistance
                        - abs(
                            abs(
                                sum(robot.drivetrain.getPositions()) / 4
                                - sum(self.startPos) / 4
                            )
                        )
                    )
                    <= 18
                ):  # Slow down when we are about eighteen inches from the goal.
                    robot.drivetrain.setUniformModulePercent(0.25)
                elif (
                    abs(
                        self.desiredDistance
                        - abs(
                            abs(
                                sum(robot.drivetrain.getPositions()) / 4
                                - sum(self.startPos) / 4
                            )
                        )
                    )
                    <= 36
                ):
                    robot.drivetrain.setUniformModulePercent(0.5)
                else:
                    robot.drivetrain.setSpeeds(
                        [
                            self.maxSpeed + speedOffset,
                            self.maxSpeed,
                            self.maxSpeed + speedOffset,
                            self.maxSpeed,
                        ]
                    )

            else:

                robot.drivetrain.setSpeeds(
                    [
                        self.maxSpeed + speedOffset,
                        self.maxSpeed,
                        self.maxSpeed + speedOffset,
                        self.maxSpeed,
                    ]
                )

    def atWaypoint(self):
        count = 0
        for position, start in zip(robot.drivetrain.getPositions(), self.startPos):
            if abs(position - (start + self.desiredDistance)) < 1 or abs(
                (position - (start + self.desiredDistance))
            ) > abs(
                self.lastDisplacement
            ):  # 1 inch is the tolerance, or have we passed it?
                print("l " + str(self.lastDisplacement))
                print(" current " + str(abs(position - (start + self.desiredDistance))))
                print("\n\nAt waypoint")  # NOTE: It's distance remaining.
                return True

        self.lastDisplacement = abs(position - (start + self.desiredDistance))
        return False

    def isFinished(self):
        return self.pathFinished

    def end(self, interrupted):
        if self.stopWhenDone:
            robot.drivetrain.stop()
