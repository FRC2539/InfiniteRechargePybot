from commands2 import CommandBase

import robot


class ConveyorIntakeForwardCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.conveyorintake)

    def initialize(self):
        robot.conveyorintake.intakeBalls()

    def end(self, interrupted):
        robot.conveyorintake.stop()
