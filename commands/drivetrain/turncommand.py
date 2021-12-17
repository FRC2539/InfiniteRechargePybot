from commands2 import CommandBase

import robot
import constants

import math

from wpimath.geometry import Rotation2d

from wpimath.kinematics import ChassisSpeeds

import constants


class TurnCommand(CommandBase):
    """Allows autonomous turning using the drive base encoders."""

    def __init__(self, degrees, tolerance=5):
        super().__init__()

        self.degrees = degrees
        self.tolerance = tolerance
        
        self.driveController = robot.drivetrain.driveController

        self.addRequirements(robot.drivetrain)

    def initialize(self):
        """Calculates new positions by offseting the current ones."""

        robot.drivetrain.setModuleProfiles(1, turn=False)

    def execute(self):
        pass

    def isFinished(self):
        return abs(robot.drivetrain.getAngleTo(self.startAngle)) + self.tolerance > abs(
            self.degrees
        )

    def end(self, interrupted):
        robot.drivetrain.stop()
        robot.drivetrain.setModuleProfiles(0, turn=False)
