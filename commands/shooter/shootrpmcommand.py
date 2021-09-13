from commands2 import CommandBase

import robot


class ShootRPMCommand(CommandBase):
    def __init__(self, val, usePercent=False):
        super().__init__()

        self.addRequirements(robot.shooter)

        self.val = val
        self.usePercent = usePercent

    def initialize(self):
        if self.usePercent:
            robot.shooter.setPercent(0.3)
        else:
            robot.shooter.setRPM(self.val)

    def end(self, interrupted):
        robot.shooter.stopShooter()
