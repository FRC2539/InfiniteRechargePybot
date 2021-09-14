from commands2 import CommandBase

import robot


class ShootRPMCommand(CommandBase):
    def __init__(self, val, usePercent=False):
        super().__init__()

        self.addRequirements(robot.shooter)

        self.val = val
        self.usePercent = usePercent

    def initialize(self):
        robot.lights.blinkWhite()
        if self.usePercent:
            robot.shooter.setPercent(0.3)
        else:
            robot.shooter.setRPM(self.val)

    def execute(self):
        if robot.shooter.getRPM() > 4000:
            print("shooter over 4400")
            robot.lights.fire()
        else:
            print("shooter under 4000")
            robot.lights.blinkWhite()

    def end(self, interrupted):
        robot.lights.blinkWhite()
        robot.shooter.stopShooter()
