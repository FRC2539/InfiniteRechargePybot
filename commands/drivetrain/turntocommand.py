from commands2 import CommandBase

from .turncommand import TurnCommand

import robot


class TurnToCommand(CommandBase):
    """Turn to a specified angle using the gyroscope."""

    def __init__(self, targetDegrees):
        """
        targetDegrees is the angle to turn to.
        """

        super().__init__()

        self.targetDegrees = targetDegrees

    def initialize(self):
        angle = robot.drivetrain.getAngleTo(self.targetDegrees)

        TurnCommand(
            angle
        ).schedule()  # Should run the command at the next CommandScheduler loop.
