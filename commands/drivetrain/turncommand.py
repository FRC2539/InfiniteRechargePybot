from .movecommand import MoveCommand

import robot

import constants

import math


class TurnCommand(MoveCommand):
    """Allows autonomous turning using the drive base encoders."""

    def __init__(self, degrees, name=None):
        if name is None:
            name = "Turn %f degrees" % degrees

        super().__init__(degrees, name=name)

        self.degrees = degrees

        # Store our initial angle
        self.initialAngle = robot.drivetrain.getAngle()

        # Set a tolerance for the angle
        self.tolerance = 0.5

    def initialize(self):
        """Calculates new positions by offseting the current ones."""

        robot.drivetrain.rotateByAngle(self.degrees)

    def isFinished(self):
        return abs(
            robot.drivetrain.getAngleTo(self.initialAngle)
        ) + self.tolerance > abs(self.degrees)
