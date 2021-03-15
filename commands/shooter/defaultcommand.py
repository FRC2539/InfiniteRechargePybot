from commands2 import CommandBase

import robot


class DefaultCommand(CommandBase):

    def __init__(self):
        super().__init__()

        self.addRequirements(robot.shooter, robot.conveyor)

    def execute(self):
        robot.shooter.setRPM(4000)
        robot.conveyor.forward()
