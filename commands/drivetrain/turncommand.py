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

        # Set a tolerance for the angle
        self.tolerance = 0.5

        self.distance = robot.drivetrain.degreesToInches(self.degrees)

        leftIsPositive = 1 if self.degrees >= 0 else -1

        # [Left, Right]
        self.targetDistances = [
            self.distance * leftIsPositive,
            self.distance * leftIsPositive * -1,
        ]

        print(self.targetDistances)

        robot.drivetrain.setMotorPositions(self.targetDistances)

    def isFinished(self):
        return abs(self.initialAngle - robot.drivetrain.getRawAngle()) <= self.tolerance

    def end(self, interrupted):
        robot.drivetrain.stop()
