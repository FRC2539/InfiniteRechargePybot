from commands2 import CommandBase

import robot


class ColorControlCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.chamber)

    def initialize(self):
        robot.chamber.spinColorWheelSlow()

    def end(self, interrupted):
        robot.chamber.stop()
