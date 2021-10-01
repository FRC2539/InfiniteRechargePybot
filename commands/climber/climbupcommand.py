from commands2 import CommandBase

import robot


class ClimbUpCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.climber)

    def execute(self):
        robot.climber.raiseClimber()

    def end(self, interrupted):
        robot.climber.stopClimber()
