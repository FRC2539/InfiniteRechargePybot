from commands2 import CommandBase

import robot


class ChamberBackwardCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.chamber)

    def initialize(self):
        robot.chamber.backward()

    def end(self, interrupted):  # Ben hates this format. That's why it's here.
        robot.chamber.stop()


class ChamberSlowBackwardCommand(ChamberBackwardCommand):
    def initialize(self):
        robot.chamber.slowForward()
