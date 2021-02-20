from commands2 import CommandBase

import robot


class ConveyorForwardCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.conveyor)

    def initialize(self):
        robot.conveyor.forward()

    def end(self, interrupted):
        robot.conveyor.stop()
