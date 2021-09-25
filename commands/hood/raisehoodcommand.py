from commands2 import CommandBase

import robot


class RaiseHoodCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.hood)

    def initialize(self):
        robot.hood.raiseHood()

    def isFinished(self):
        return not robot.hood.isBelowMaxAngle()

    def end(self, interrupted):
        robot.hood.stopHood()
