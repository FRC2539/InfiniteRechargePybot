from commands2 import CommandBase

import robot


class RaiseHoodCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.hood)

    def execute(self):
        robot.hood.raiseHood()

    def end(self, interrupted):
        robot.hood.stopHood()
