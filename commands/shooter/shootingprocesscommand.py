from commands2 import CommandBase

from wpilib import Timer

import robot


class ShootingProcessCommand(CommandBase):
    """Gets the shooter up to speed, then moves the ball through the robot and shoot them."""

    def __init__(
        self,
        targetRPM=5000,
        tolerance=50,
        ballCount=-1,
        delay=0.5,
        delayConveyor=False,
        wait=False,
    ):

        super().__init__()

        self.targetRPM = targetRPM
        self.tolerance = tolerance
        self.delay = delay
        self.delayConveyor = delayConveyor
        self.wait = wait

        self.isAtTargetRPM = False
        self.enableTimer = False
        self.timerStarted = False

        self.found = False
        self.ballCount = ballCount

        self.lastBallTimer = Timer()

        self.addRequirements([robot.conveyorintake, robot.chamber])

    def initialize(self):
        if not self.delayConveyor:
            robot.conveyorintake.intakeBalls()
        else:
            robot.conveyorintake.stop()
        robot.shooter.setRPM(self.targetRPM)

    def execute(self):
        print('running shoot')
        robot.shooter.setRPM(self.targetRPM)
        self.checkRPM()

        if self.isAtTargetRPM and not self.wait:
            robot.conveyorintake.intakeBalls()
            robot.chamber.forward()

        elif self.isAtTargetRPM and robot.limelight.isAimed() and robot.limelight.getTape():
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
        if self.ballCount != -1 and robot.chamber.isBallPresent() and not self.found:
            self.ballCount -= 1
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
