from commands2 import CommandBase

import robot


class LowerClimberCommand(CommandBase):
    """
    Lowers the climber, allowing us to elevate ourselves.
    """

    def __init__(self):
        super().__init__()

        self.addRequirements(robot.climber)

    def initialize(self):
        robot.climber.lowerClimber()

    def execute(self):
        robot.climber.lowerClimber()

    def end(self, interrupted):
        robot.climber.stopClimber()
