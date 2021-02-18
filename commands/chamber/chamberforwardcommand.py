from commands2 import CommandBase

import robot


class ChamberForwardCommand(CommandBase):

    def __init__(self):
        super().__init__()

        self.addRequirements(robot.chamber)

    def initialize(self):
        robot.chamber.forward()

    def end(
            self,
            interrupted
        ):
        robot.chamber.stop()

class ChamberSlowForwardCommand(ChamberForwardCommand):

    def initialize(self):
        robot.chamber.slowForward()
