from commands2 import CommandBase

import robot


class ForceClimbDownCommand(CommandBase):
    """
    Forcefully and slowly lowers the climber, overriding any
    limits that may exist.
    """

    def __init__(self):
        super().__init__()

        self.addRequirements(robot.climber)

    def execute(self):
        robot.climber.forceLowerClimber()

    def end(self, interrupted):
        robot.climber.stopClimber()
