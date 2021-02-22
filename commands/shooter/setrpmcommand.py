from commands2 import CommandBase

import robot


class SetRPMCommand(CommandBase):
    """Speeds up the shooter to the target RPM."""

    def __init__(self, targetRPM=5000):

        super().__init__()

        self.targetRPM = targetRPM

        self.addRequirements(robot.shooter)

    def initialize(self):
        robot.shooter.setRPM(self.targetRPM)

    def end(self, interrupted):
        robot.shooter.stopShooter()
