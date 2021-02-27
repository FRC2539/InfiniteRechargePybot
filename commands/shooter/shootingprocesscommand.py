from commands2 import CommandBase

import robot


class ShootingProcessCommand(CommandBase):
    """Gets the shooter up to speed, then moves the ball through the robot and shoot them."""

    def __init__(self, targetRPM=5000):

        super().__init__()

        self.targetRPM = targetRPM

        self.isAtTargetRPM = False

        self.addRequirements([robot.conveyor, robot.chamber])

    def initialize(self):
        robot.shooter.setRPM(self.targetRPM)

    def execute(self):
        self.checkRPM()

        if self.isAtTargetRPM:
            robot.conveyor.forward()
            robot.chamber.forward()

    def checkRPM(self):
        if not self.isAtTargetRPM and robot.shooter.getRPM() >= self.targetRPM:
            self.isAtTargetRPM = True

    def end(self, interrupted):
        robot.conveyor.stop()
        robot.chamber.stop()
        robot.shooter.stopShooter()
