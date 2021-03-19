from commands2 import InstantCommand

import robot
import constants


class SetSpeedCommand(InstantCommand):
    """Changes the max speed of the drive subsystem."""

    def __init__(self, speed=True):
        super().__init__()

        if speed:  # Sets to normal speed.
            self.speed = constants.drivetrain.speedLimit

        else:  # Sets to slow speed.
            self.speed = constants.drivetrain.speedLimit * 0.3

    def initialize(self):
        robot.drivetrain.setSpeedLimit(self.speed)
