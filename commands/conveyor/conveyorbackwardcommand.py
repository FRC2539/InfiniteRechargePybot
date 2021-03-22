from commands2 import CommandBase

import robot


class ConveyorBackwardCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements([robot.conveyor])

    def initialize(self):
        robot.conveyor.backward()

    def execute(self):
        robot.conveyor.backward()

    def end(self, interrupted):
        robot.conveyor.stop()
