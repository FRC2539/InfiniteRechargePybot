from commands2 import CommandBase

from wpilib import RobotBase

import math, os, inspect
import robot


class RunAutoCommand(CommandBase):
    def __init__(self, points: int = 1, tolerance=1, angleTol=3):
        """
        Distance is the distance we should travel in inches, turnOffset
        is the angle displacement of the gyro in degrees.
        """

        super().__init__()

        self.addRequirements([robot.drivetrain])
        
        if RobotBase.isSimulation():
            pass
        
        else:
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
                    if str(line).strip() == "|||": # Exit when at the end of the trajectory.
                        break
                    self.allPoints.append(eval(line))

                f.close()
            
        self.speeds = self.allPoints[0]
        self.angles = self.allPoints[1]

        self.tolerance = tolerance
        self.angleTol = angleTol

    def initialize(self):
        robot.drivetrain.setModuleProfiles(0, drive=False)

        self.cycleCount = 0

    def execute(self):
        for speed, angle in zip(self.speeds, self.angles):
            robot.drivetrain.setModuleAngles(angle)
            robot.drivetrain.setModuleSpeed(speed)
            self.cycleCount += 1

    def isFinished(self):
        return self.cycleCount == len(self.speeds) # It doesn't matter if we use speeds or angles here.

    def end(self, interrupted):
        robot.drivetrain.stop()
