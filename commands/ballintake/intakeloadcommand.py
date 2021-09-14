from commands2 import CommandBase

import robot

from wpilib import Timer


class IntakeLoadCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.ballintake)

        # Tracks whether the ball is present or not
        self.ballIsPresent = False
        self.runningInternalBallSystem = False

        # Create a timer to run the intake for
        # set amounts of time
        self.timer = Timer()

        self.moveBallInterval = 0.5  # seconds

        # FIX: doesn't stop on first ball, doesn't intake second ball

    def initialize(self):
        robot.lights.solidGreen()
        robot.ballintake.forwardIntake()

    def execute(self):
        self.ballIsPresent = robot.ballintake.isBallPresent()

        print(f"Ball is present: {self.ballIsPresent}")

        if self.ballIsPresent and not self.runningInternalBallSystem:
            # Runs the internal ball system when
            # there is a ball in the intake
            robot.ballintake.forwardConveyor()
            robot.ballintake.forwardShooterFeed()

            # Update the robot state
            self.runningInternalBallSystem = True

            # Reset and start the timer
            self.timer.reset()
            self.timer.start()

        if (
            not self.ballIsPresent
            and self.runningInternalBallSystem
            and self.isTimeToStopIntake()
        ):
            # Stops the internal intake when no ball is present
            robot.ballintake.stopConveyor()
            robot.ballintake.stopShooterFeed()

            # Update the robot state
            self.runningInternalBallSystem = False

    def isTimeToStopIntake(self):
        """
        Determines if enough time has passed to stop
        moving a ball through the internal intake
        """
        return self.timer.get() >= self.moveBallInterval

    def end(self, interrupted):
        robot.lights.off()
        robot.ballintake.stopAll()
