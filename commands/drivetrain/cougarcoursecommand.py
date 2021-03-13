from commands2 import CommandBase

from wpilib import RobotBase

import math, os, inspect
import robot


class CougarCourseCommand(CommandBase):
    def __init__(self, points, tolerance=1, angleTol=3):
        """
        Distance is the distance we should travel in inches, turnOffset
        is the angle displacement of the gyro in degrees.
        """

        super().__init__()

        self.addRequirements([robot.drivetrain])
        if RobotBase.isSimulation():
            pass

        elif type(points) == int:
            self.allPoints = []
            with open(
                (os.path.dirname(robot.__file__) + "/trajectorydata.txt"), "r"
            ) as f:
                index = 0
                f_ = list(f)

                id_ = f_[index]
                while id_ != str(points):
                    try:
                        id_ = f_[index].strip()
                    except (IndexError):
                        raise Exception(
                            "Make sure ID of constants matches the auto ID."
                        )
                    index += 1

                for line in f_[index:]:
                    if str(line).strip() == "|||":
                        break
                    self.allPoints.append(eval(line))

                f.close()
        else:
            additionalPoints = robot.drivetrain.injectPoints(points)
            self.allPoints = robot.drivetrain.smoothPoints(additionalPoints)
            self.allPoints = robot.drivetrain.assertDistanceAlongCurve(self.allPoints)

        self.tolerance = tolerance
        self.angleTol = angleTol

    def initialize(self):
        self.startAngle = robot.drivetrain.getAngle()
        robot.drivetrain.setModuleProfiles(0, drive=False)

        robot.drivetrain.resetOdometry()
        self.lastPosX = robot.drivetrain.getSwervePose().X() * 39.3701
        self.lastPosY = robot.drivetrain.getSwervePose().Y() * 39.3701

        self.start = sum(robot.drivetrain.getPositions()) / len(
            robot.drivetrain.getPositions()
        )

        self.inchesTravelledX = 0
        self.inchesTravelledY = 0

        self.lookAheadInches = 12

        self.angleSet = False

    def execute(self):
        self.inchesTravelledX = (
            robot.drivetrain.getSwervePose().X() * 39.3701
            - self.lastPosX
            + self.inchesTravelledX
        )
        self.inchesTravelledY = (
            robot.drivetrain.getSwervePose().Y() * 39.3701
            - self.lastPosY
            + self.inchesTravelledY
        )
        self.displacement = (
            sum(robot.drivetrain.getPositions()) / len(robot.drivetrain.getPositions())
            - self.start
        )
        # math.sqrt(self.inchesTravelledX**2 + self.inchesTravelledY**2)

        self.nextDistance = self.displacement + self.lookAheadInches

        for point in self.allPoints:
            self.currentX = point[0]
            self.currentY = point[1]
            if point[3] > self.displacement:
                break
        # self.currentX = robot.drivetrain.getSwervePose().X() *39.3701
        # self.currentY = robot.drivetrain.getSwervePose().Y() *39.3701

        for point in self.allPoints:
            self.targetX = point[0]
            self.targetY = point[1]
            self.targetV = point[2]
            if point[3] > self.nextDistance:
                break

        theta = (
            math.degrees(
                math.atan2(
                    (self.targetY - self.currentY), (self.targetX - self.currentX)
                )
            )
            + 90
        )

        self.kP = 0.2
        gyroOffset = robot.drivetrain.getAngleTo(self.startAngle)
        #print("go " + str(gyroOffset))

        # Populate a matrix corresponding to the desired velocity.
        speedsMatrix = [[self.targetV, self.targetV], [self.targetV, self.targetV]]

        # Populate a matrix with the wheel angles that need to have their speed increased.
        # This will be determined by the gyro's offset.
        idMatrix = [[1, 0], [1, 0]]

        if gyroOffset < 0:
            idMatrix = [[0, 1], [0, 1]]

        # Rotate the matrix based on the offset.
        for i in range(round((theta) / 90)):  # (360-theta)/90
            idMatrix = list(zip(*idMatrix))[::-1]

        # Add p to the id matrix and element-wise multiply the wheel speed matrix by that
        for i in range(len(speedsMatrix)):
            for j in range(len(speedsMatrix[i])):
                speedsMatrix[i][j] += speedsMatrix[i][j] * idMatrix[i][j] * self.kP

        newSpeeds = []
        speedsMatrix.reverse()
        for l in speedsMatrix:
            l.reverse()
            for speed in l:
                newSpeeds.append(speed)

        toTravel = self.nextDistance - self.displacement

        robot.drivetrain.setUniformModuleAngle(theta)

        if (
            not self.angleSet
            and max(
                [abs(angle - theta) for angle in robot.drivetrain.getModuleAngles()]
            )
            <= self.angleTol
        ):
            self.angleSet = True

        elif self.angleSet:
            robot.drivetrain.setSpeeds(self.targetV)#newSpeeds)
        # robot.drivetrain.move(ErrorX* .1, ErrorY*.1, angleError*-.01)

    def isFinished(self):
        return self.displacement > self.allPoints[-1][3]

    def end(self, interrupted):
        robot.drivetrain.stop()
