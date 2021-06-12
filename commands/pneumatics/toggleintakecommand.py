from commands2 import InstantCommand

import robot


class ToggleIntakeCommand(InstantCommand):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.pneumatics)

    def initialize(self):
        robot.pneumatics.toggleIntake()
