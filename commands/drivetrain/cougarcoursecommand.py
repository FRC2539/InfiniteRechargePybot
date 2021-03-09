from commands2 import CommandBase

from wpilib import RobotBase

import math, os, inspect
import robot


class CougarCourseCommand(CommandBase):
    def __init__(self, points, tolerance=1):
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
                    id_ = f_[index].strip()
                    index += 1
                    
                for line in f_[index:]:
                    if str(line).strip() == '|||':
                        break
                    self.allPoints.append(eval(line))

                f.close()
        else:
            additionalPoints = robot.drivetrain.injectPoints(points)
            self.allPoints = robot.drivetrain.smoothPoints(additionalPoints)
            self.allPoints = robot.drivetrain.assertDistanceAlongCurve(self.allPoints)

        self.tolerance = tolerance
        
    def initialize(self):
        robot.drivetrain.setModuleProfiles(0, drive=False)

        robot.drivetrain.resetOdometry()
        self.lastPosX = robot.drivetrain.getSwervePose().X() * 39.3701
        self.lastPosY = robot.drivetrain.getSwervePose().Y() * 39.3701

        self.start = sum(robot.drivetrain.getPositions()) / len(
            robot.drivetrain.getPositions()
        )

        self.inchesTravelledX = 0
        self.inchesTravelledY = 0

        self.lookAheadInches = 6

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

        for point in self.allPoints:
            self.targetX = point[0]
            self.targetY = point[1]
            self.targetV = point[2]
            if point[3] > self.nextDistance:
                break

        theta = math.degrees(
            math.atan2((self.targetY - self.currentY), (self.targetX - self.currentX))
        )

        toTravel = self.nextDistance - self.displacement
        #print(theta)
        #print(str(self.targetX) + str(self.targetY))
        robot.drivetrain.setUniformModuleAngle(theta + 90)
        robot.drivetrain.setUniformModuleSpeeds(self.targetV)


    def isFinished(self):
        return self.displacement > self.allPoints[-1][3]

    def end(self, interrupted):
        robot.drivetrain.stop()
