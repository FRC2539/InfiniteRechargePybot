from commands2 import CommandBase

import robot

import constants


class IntakeLoadCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.ballintake)

        # Tracks whether the ball is present and where it is
        self.intakeBallIsPresent = False
        self.conveyorBallIsPresent = False
        self.shooterBallIsPresent = False

    def initialize(self):
        robot.lights.solidGreen()
        robot.ballintake.forwardIntake()

        # Store the current speed limit
        self.currentSpeedLimit = robot.drivetrain.getSpeedLimit()

        # Update the speed limit to be slower while intaking
        robot.drivetrain.setSpeedLimit(constants.drivetrain.intakeSpeedLimit)

    def execute(self):
        # Read the values from the sensors
        self.updateSensorReadings()

        if self.shooterBallIsPresent and not self.intakeBallIsPresent:
            # Runs the intake motor to intake balls
            robot.ballintake.forwardIntake()
            robot.ballintake.stopConveyor()
            robot.ballintake.stopShooterFeed()

        elif self.intakeBallIsPresent and self.shooterBallIsPresent:
            robot.ballintake.stopIntake()
            robot.ballintake.stopConveyor()
            robot.ballintake.stopShooterFeed()

        elif self.intakeBallIsPresent and not self.shooterBallIsPresent:
            # Runs the internal ball system when
            # there is a ball in the intake
            robot.ballintake.forwardConveyor()
            robot.ballintake.forwardShooterFeed()

        elif (
            not self.intakeBallIsPresent
            and not self.conveyorBallIsPresent
            and not self.shooterBallIsPresent
        ):
            # Stops the internal intake when no ball is present
            robot.ballintake.stopConveyor()
            robot.ballintake.stopShooterFeed()

    def updateSensorReadings(self):
        """
        Update the state of the ball sensors
        """
        self.intakeBallIsPresent = robot.ballintake.isIntakeBallPresent()
        self.conveyorBallIsPresent = robot.ballintake.isConveyorBallPresent()
        self.shooterBallIsPresent = robot.ballintake.isShooterBallPresent()

    def end(self, interrupted):
        robot.lights.off()
        robot.ballintake.stopAll()
        robot.drivetrain.setSpeedLimit(self.currentSpeedLimit)
