from commands2 import CommandBase

import robot


class ShootingProcessCommand(CommandBase):
    """Gets the shooter up to speed, then moves the ball through the robot and shoot them."""

    def __init__(self, targetRPM=5000, tolerance=50):

        super().__init__()

        self.targetRPM = targetRPM
        self.tolerance = tolerance

        self.isAtTargetRPM = False

        self.addRequirements([robot.conveyorintake, robot.chamber])

    def initialize(self):
        robot.conveyorintake.intakeBalls()
        robot.shooter.setRPM(self.targetRPM)

    def execute(self):
        self.checkRPM()

        if self.isAtTargetRPM:
            print("at target")
            robot.conveyorintake.intakeBalls()
            robot.chamber.forward()

    def checkRPM(self):
        if (
            not self.isAtTargetRPM
            and abs(robot.shooter.getRPM() - self.targetRPM) <= self.tolerance
        ):
            self.isAtTargetRPM = True
        else:
            self.isAtTargetRPM = False

    def isFinished(self):
        return False

    def end(self, interrupted):
        robot.conveyorintake.stop()
        robot.chamber.stop()
        robot.shooter.stopShooter()
