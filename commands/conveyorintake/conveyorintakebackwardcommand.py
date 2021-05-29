from commands2 import CommandBase

import robot


class ConveyorIntakeBackwardCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.conveyorintake)

    def initialize(self):
        robot.conveyorintake.outtakeBalls()

    def execute(self):
        robot.conveyorintake.outtakeBalls()

    def end(self, interrupted):
        robot.conveyorintake.stop()
