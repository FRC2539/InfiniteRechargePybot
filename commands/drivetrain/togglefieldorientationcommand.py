from commands2 import InstantCommand

import robot


class ToggleFieldOrientationCommand(InstantCommand):
    def __init__(self, set_=None):
        super().__init__()

        self.addRequirements(robot.drivetrain)

        self.set_ = set_

    def initialize(self):
        if self.set_ is None:
            robot.drivetrain.isFieldOriented = not robot.drivetrain.isFieldOriented
        else:
            robot.drivetrain.isFieldOriented = self.set_
