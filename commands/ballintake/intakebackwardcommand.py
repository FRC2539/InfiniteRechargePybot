from commands2 import CommandBase

import robot


class IntakeBackwardCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.ballintake)

    def initialize(self):
        robot.ballintake.backwardAll()

    def end(self, interrupted):
        robot.ballintake.stopAll()
