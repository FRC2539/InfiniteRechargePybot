from commands2 import CommandBase

import robot


class RaiseHoodCommand(CommandBase):
    """
    Manually raises the hood. Technically,
    this lowers the apex of the shots.
    """

    def __init__(self):
        super().__init__()
        self.addRequirements(robot.hood)

    def execute(self):
        print("raising")
        robot.hood.move(robot.hood.speed)

    def end(self, cheese):
        robot.hood.stop()
