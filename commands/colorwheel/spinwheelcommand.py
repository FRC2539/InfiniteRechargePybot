from commands2 import CommandBase

import robot


class SpinWheelCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.chamber)

    def initialize(self):
        robot.chamber.spinColorWheel()

    def end(self, interrupted):
        robot.chamber.stop()
