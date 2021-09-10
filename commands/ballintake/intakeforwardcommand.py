from commands2 import CommandBase

import robot


class IntakeForwardCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.ballintake)

    def initialize(self):
        robot.ballintake.forwardAll()

    def end(self, interrupted):
        robot.ballintake.stopAll()
