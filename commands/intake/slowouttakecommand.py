from commands2 import CommandBase
import robot


class SlowOuttakeCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.intake)

    def initialize(self):
        robot.intake.slowOut()

    def end(self, interrupted):
        robot.intake.dontIntakeBalls()
