from commands2 import CommandBase

import robot


class DefaultCommand(CommandBase):

    def __init__(self):
        super().__init__()

        self.addRequirements(robot.shooter)
        self.addRequirements(robot.conveyor)

    def execute(self):
        robot.conveyor.forward()
        robot.shooter.setRPM(4200)
            
    def end(self, interrupted):
        robot.shooter.stopShooter()
        robot.conveyor.stop()
