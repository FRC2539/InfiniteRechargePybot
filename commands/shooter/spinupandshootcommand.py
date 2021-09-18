from commands2 import CommandBase

import robot


class SpinUpAndShootCommand(CommandBase):
    def __init__(self, targetRPM, rpmTolerance=100):
        super().__init__()

        # Requires the intake and shooter subsystems
        self.addRequirements([robot.ballintake, robot.shooter])

        self.targetRPM = targetRPM

        self.rpmTolerance = rpmTolerance

        # Keep track of the state of the shooter
        self.isUpToSpeed = False

    def initialize(self):
        robot.shooter.setRPM(self.targetRPM)

    def execute(self):
        self.checkForNewShooterSpeed()

        # Run the balls through the shooter
        # once the shooter is  up to speed
        if self.isUpToSpeed:
            robot.ballintake.forwardAll()

    def checkForNewShooterSpeed(self):
        # Finds the error between the
        # target rpm and the rpm we are at
        # and see if it is within our tolerance
        self.isUpToSpeed = (
            abs(robot.shooter.getRPM() - self.targetRPM) <= self.rpmTolerance
        )

    def end(self, interrupted):
        # Stop the shooter and intake
        robot.shooter.stopShooter()
        robot.ballintake.stopAll()
