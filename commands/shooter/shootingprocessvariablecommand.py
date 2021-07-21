from commands2 import CommandBase

from wpilib import Timer

import robot


class ShootingProcessVariableCommand(CommandBase):
    """Gets the shooter up to speed, then moves the ball through the robot and shoot them."""

    def __init__(
        self, intakeSpeed, targetRPM=5000, tolerance=50, ballCount=-1, delay=0.5
    ):

        super().__init__()

        self.intakeSpeed = intakeSpeed
        self.targetRPM = targetRPM
        self.tolerance = tolerance

        self.delay = delay

        self.isAtTargetRPM = False
        self.enableTimer = False
        self.timerStarted = False

        self.found = False
        self.ballCount = ballCount

        self.lastBallTimer = Timer()

        self.addRequirements([robot.conveyorintake, robot.chamber])

    def initialize(self):
        robot.conveyorintake.move(self.intakeSpeed)
        robot.shooter.setRPM(self.targetRPM)

    def execute(self):
        self.checkRPM()

        if self.isAtTargetRPM:
            robot.conveyorintake.move(self.intakeSpeed)
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
        if self.ballCount != -1 and robot.chamber.isBallPresent() and not self.found:
            self.ballCount -= 1
            print("remaining " + str(self.ballCount))
            self.found = True
            if self.ballCount == 0:
                self.enableTimer = True
        elif not robot.chamber.isBallPresent():
            self.found = False
        else:
            return False

        if self.enableTimer and not self.timerStarted:
            self.lastBallTimer.start()
            self.timerStarted = True

        if self.timerStarted and self.lastBallTimer.get() > self.delay:
            self.lastBallTimer.stop()
            self.lastBallTimer.reset()
            return True

    def end(self, interrupted):
        robot.conveyorintake.stop()
        robot.chamber.stop()
        robot.shooter.stopShooter()
