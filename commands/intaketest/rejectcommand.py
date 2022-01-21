from commands2 import CommandBase

import robot


class RejectCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.intaketest)

    def initialize(self):
        robot.intaketest.outtakeBalls()

    def end(self, interrupted):
        robot.intaketest.stop()
