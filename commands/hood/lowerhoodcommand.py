from commands2 import CommandBase

import robot


class LowerHoodCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.hood)

    def execute(self):
        robot.hood.lowerHood()

    def end(self, interrupted):
        robot.hood.stopHood()
