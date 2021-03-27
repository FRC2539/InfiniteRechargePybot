from commands2 import CommandBase

from controller import logicalaxes
import robot

logicalaxes.registerAxis("TURRETmOVE")


class DefaultCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.turret)

    def execute(self):
        speed = logicalaxes.TURRETmOVE.get() * -0.3
        print('moving')
        robot.turret.move(speed)

    def end(self, cheeseball):
        robot.turret.stop()
