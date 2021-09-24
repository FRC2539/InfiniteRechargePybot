from commands2 import CommandBase

import robot


class IntakeLoadCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.ballintake)

        # Tracks whether the ball is present and where it is
        self.intakeBallIsPresent = False
        self.conveyorBallIsPresent = False
        self.shooterBallIsPresent = False

    def initialize(self):
        print("init intake")
        robot.lights.solidGreen()
        robot.ballintake.forwardIntake()

    def execute(self):
        # Read the values from the sensors
        self.updateSensorReadings()

        if self.shooterBallIsPresent and not self.intakeBallIsPresent:
            print("stage 1")
            robot.ballintake.forwardIntake()
            robot.ballintake.stopConveyor()
            robot.ballintake.stopShooterFeed()

        elif self.intakeBallIsPresent and self.shooterBallIsPresent:
            print("stage 2")
            robot.ballintake.stopIntake()
            robot.ballintake.stopConveyor()
            robot.ballintake.stopShooterFeed()

        elif self.intakeBallIsPresent and not self.shooterBallIsPresent:
            print("stage 3")
            # Runs the internal ball system when
            # there is a ball in the intake
            robot.ballintake.forwardConveyor()
            robot.ballintake.forwardShooterFeed()

        elif (
            not self.intakeBallIsPresent
            and not self.conveyorBallIsPresent
            and not self.shooterBallIsPresent
        ):
            print("else")
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
