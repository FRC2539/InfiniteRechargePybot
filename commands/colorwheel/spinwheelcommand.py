from commands2 import CommandBase

import robot


class SpinWheelCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.colorwheel)

    def execute(self):
        robot.colorwheel.spin()

    def end(self, interrupted):
        robot.colorwheel.stopSpinner()
