from commands2 import CommandBase

import robot

from wpilib import Timer


class IntakeLoadCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.ballintake)

        # Tracks whether the ball is present and where it is
        self.intakeBallIsPresent = False
        self.conveyorBallIsPresent = False

    def initialize(self):
        robot.lights.solidGreen()
        robot.ballintake.forwardIntake()

    def execute(self):
        # Read the values from the sensors
        self.updateSensorReadings()

        if self.intakeBallIsPresent:
            # Runs the internal ball system when
            # there is a ball in the intake
            robot.ballintake.forwardConveyor()
            robot.ballintake.forwardShooterFeed()

        elif not self.intakeBallIsPresent and not self.conveyorBallIsPresent:

            # Stops the internal intake when no ball is present
            robot.ballintake.stopConveyor()
            robot.ballintake.stopShooterFeed()

    def updateSensorReadings(self):
        """
        Update the state of the ball sensors
        """
        self.intakeBallIsPresent = robot.ballintake.isIntakeBallPresent()
        self.conveyorBallIsPresent = robot.ballintake.isConveyorBallPresent()

    def end(self, interrupted):
        robot.lights.off()
        robot.ballintake.stopAll()
