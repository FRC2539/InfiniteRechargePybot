from commands2 import InstantCommand

import robot


class ResetTiltCommand(InstantCommand):
    def __init__(self):
        super().__init__()

        self.requires(robot.drivetrain)
        self.setRunWhenDisabled(True)

    def initialize(self):
        robot.drivetrain.resetTilt()
