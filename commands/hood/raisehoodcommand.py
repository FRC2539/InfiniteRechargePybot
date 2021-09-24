from commands2 import CommandBase

import robot


class RaiseHoodCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.shooter)

    def initialize(self):
        robot.hood.raiseHood()

    def isFinished(self):
        # print(robot.hood.getPosition())
        if robot.hood.atHighest():
            robot.hood.stopHood()
            return True
        else:
            return False

    def end(self):
        robot.hood.stopHood()
        # print('\n\n\n\nDONE\n\n\n\n')
