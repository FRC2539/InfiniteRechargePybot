from commands2 import CommandBase

import robot


class LowerHoodCommand(CommandBase):
    """
    Manually lowers the hood. Technically,
    this raises the apex of the shots.
    """

    def __init__(self):
        super().__init__()
        self.addRequirements(robot.hood)

    def execute(self):
        robot.hood.move(-robot.hood.speed)

    def end(self, cheese):
        robot.hood.stop()
