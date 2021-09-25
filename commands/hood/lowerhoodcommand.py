from commands2 import CommandBase

import robot


class LowerHoodCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.hood)

    def initialize(self):
        hood.lowerHood()

    def isFinished(self):
        return not hood.isWithinBounds()

    def end(self, interrupted):
        hood.stopHood()
