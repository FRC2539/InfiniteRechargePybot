from .movecommand import MoveCommand

import robot

# from custom.config import Config

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

        distance = self._calculateDisplacement()

        targetPositions = []

        # Flip the sign for every other motor
        sign = 1

        # Calculate all of the target positions for the rotation
        for position in robot.drivetrain.getPositions():
            targetPositions.append(position + (distance * sign))
            sign *= -1

        robot.drivetrain.setMotorPositions(targetPositions)

    def isFinished(self):
        return abs(
            robot.drivetrain.getAngleTo(self.initialAngle)
        ) + self.tolerance > abs(self.degrees)

    def _calculateDisplacement(self):
        """
        In order to avoid having a separate ticksPerDegree, we calculate it
        based on the width of the robot base.
        """

        inchesPerDegree = math.pi * constants.drivetrain.robotWidth / 360

        totalDistanceInInches = self.distance * inchesPerDegree

        return totalDistanceInInches
