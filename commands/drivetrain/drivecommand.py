from commands2 import CommandBase

import constants
import robot
from controller import logicalaxes
from custom.config import Config, MissingConfigError
from custom import driverhud
import math


logicalaxes.registerAxis("forward")
logicalaxes.registerAxis("strafe")
logicalaxes.registerAxis("rotate")


class DriveCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.drivetrain)

        robot.drivetrain.resetGyro()
        robot.drivetrain.resetOdometry()

        if constants.drivetrain.swerveStyle:
            self.execute = self.swerveExecute
        else:
            self.execute = self.tankExecute

    def initialize(self):
        robot.drivetrain.stop()
        robot.drivetrain.setProfile(0)

        self.lastY = None
        self.slowed = False

    def swerveExecute(self):
        # Avoid quick changes in direction
        y = logicalaxes.forward.get()
        if self.lastY is None:
            self.lastY = y
        else:
            cooldown = 0.05
            self.lastY -= math.copysign(cooldown, self.lastY)

            # If the sign has changed, don't move
            if self.lastY * y < 0:
                y = 0

            if abs(y) > abs(self.lastY):
                self.lastY = y

        robot.drivetrain.move(
            logicalaxes.strafe.get(), y, logicalaxes.rotate.get() * 0.9
        )

    def tankExecute(self):
        # Avoid quick changes in direction
        y = logicalaxes.forward.get()
        if self.lastY is None:
            self.lastY = y
        else:
            cooldown = 0.05
            self.lastY -= math.copysign(cooldown, self.lastY)

            # If the sign has changed, don't move
            if self.lastY * y < 0:
                y = 0

            if abs(y) > abs(self.lastY):
                self.lastY = y

        robot.drivetrain.move(-y, logicalaxes.rotate.get() * -0.7)
