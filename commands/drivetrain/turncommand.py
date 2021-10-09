from commands2 import CommandBase

# from .movecommand import MoveCommand

import robot


class TurnCommand(CommandBase):
    """Allows autonomous turning using the drive base encoders."""

    def __init__(self, degrees):
        super().__init__()

        self.addRequirements(robot.drivetrain)

        self.degrees = degrees

    def initialize(self):
        # Store our initial angle
        self.initialAngle = robot.drivetrain.getRawAngle()

        # Store our initial motor positions in inches
        self.initialPositions = robot.drivetrain.getPositions()

        # Set a tolerance for the angle
        self.tolerance = 5

        self.distance = robot.drivetrain.degreesToInches(self.degrees)

        # [Front Left, Front Right, Back Left, Back Right]
        self.targetDistances = [
            self.distance,
            self.distance,
            self.distance,
            self.distance,
        ]

        # Try to divide by 2 and change wheel diameter back

        # self.targetDistances = [
        #     43.59,
        #     43.59,
        #     43.59,
        #     43.59,
        # ]

        robot.drivetrain.setMotorPositions(self.targetDistances)

    def isFinished(self):
        # Get the motor positions in inches
        motorPositions = robot.drivetrain.getPositions()

        if self.distance >= 0:
            # calculate the distance using 6 in rather than 4 in
            print(motorPositions[1], self.initialPositions[1], self.distance)

            return motorPositions[0] >= self.initialPositions[0] + self.distance
        else:
            return motorPositions[0] <= self.initialPositions[0] + self.distance

        # if
        # return abs(self.initialAngle - robot.drivetrain.getRawAngle()) + (
        #     self.tolerance / 2
        # ) >= abs(self.degrees)

    def end(self, interrupted):
        robot.drivetrain.stop()
