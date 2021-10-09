from commands2 import CommandBase

import robot


class AimWithLimelightCommand(CommandBase):
    def __init__(self, tolerance=0.3):
        super().__init__()

        self.addRequirements([robot.limelight, robot.drivetrain])

        # How close we should get to the angle before we say good enough
        # (Accounts for oscilation)
        self.tolerance = tolerance

        # Multiplied by the error to find how much to move the motor
        self.errorPercent = 0.25

        # Set a speed to aim at
        self.aimSpeed = 40

        # Track where we need to move the robot to aim
        self.xOffset = 0

        self.isAimed = False

    def initialize(self):
        self.xOffset = robot.limelight.getX()

        self.isAimed = abs(self.xOffset) <= self.tolerance

        # We don't need to aim
        if self.isAimed:
            pass

        # Account for if the offset is negative
        sign = -1 if self.xOffset < 0 else 1

        # Scale the offset
        self.xOffset *= self.errorPercent

        # Limit the offset to a maximum speed of 0.25
        self.xOffset = sign * min(abs(self.xOffset), 0.3)

        robot.drivetrain.move(0, 0, self.xOffset, customSpeed=self.aimSpeed)

    def execute(self):
        self.xOffset = robot.limelight.getX()

        self.isAimed = abs(self.xOffset) <= self.tolerance

    def isFinished(self):
        return self.isAimed

    def end(self, interrupted):
        robot.drivetrain.stop()
