from commands2 import CommandBase

import robot
import math


class TurretLimelightCommand(CommandBase):
    """Controls the turret with input from the limelight."""

    def __init__(self):
        super().__init__()

        self.addRequirements(robot.turret)

        self.xOffsetP = (
            0.050  # A proportion to scale the error to a speed the motor can use.
        )

    def initialize(self):
        robot.limelight.setPipeline(0)

    def execute(self):
        xOffset = robot.limelight.getX()  # Returns an angle

        xPercentError = xOffset * self.xOffsetP  # This value is found experimentally

        if abs(xPercentError) > 0.25:
            xPercentError = math.copysign(0.5, xPercentError)

        print('moving ' + str(xPercentError))

        robot.turret.move(xPercentError)

    def end(self, interrupted):
        robot.turret.stop()
