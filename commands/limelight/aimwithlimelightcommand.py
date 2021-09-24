from commands2 import CommandBase

import robot


class AimWithLimelightCommand(CommandBase):
    def __init__(self, tolerance=0.5):
        super().__init__()

        self.addRequirements([robot.limelight, robot.drivetrain])

        # How close we should get to the angle before we say good enough
        # (Accounts for oscilation)
        self.tolerance = 0.5

        # Track where we need to move the robot to aim
        self.xOffset = 0

        self.isAimed = False

    def initialize(self):
        robot.limelight.setPipeline(0)

        self.xOffset = robot.limelight.getX()

        self.isAimed = abs(xOffset) <= self.tolerance

        # We don't need to aim
        if self.isAimed:
            pass

        # Correct by going in the opposite direction of the offset
        robot.drivetrain.rotateByAngle(-1 * self.xOffset)

    def isFinished(self):
        return self.isAimed

    def end(self, interrupted):
        robot.drivetrain.stop()
