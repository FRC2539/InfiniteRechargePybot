from commands2 import CommandBase

import robot


class LowerHoodCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.hood)

    def initialize(self):
        robot.hood.lowerHood()

    def isFinished(self):
        return not robot.hood.isAboveMinAngle()

    def end(self, interrupted):
        robot.hood.stopHood()
