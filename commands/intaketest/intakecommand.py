from commands2 import CommandBase

import robot


class IntakeCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.intaketest)

    def initialize(self):
        robot.intaketest.intakeBalls()

    def end(self, interrupted):
        robot.intaketest.stop()
