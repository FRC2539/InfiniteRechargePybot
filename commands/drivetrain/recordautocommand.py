from commands2 import CommandBase

import constants
import robot
from controller import logicalaxes
from custom.config import Config, MissingConfigError
from custom import driverhud
import math, sys, os


logicalaxes.registerAxis("forward")
logicalaxes.registerAxis("strafe")
logicalaxes.registerAxis("rotate")


class RecordAutoCommand(CommandBase):
    def __init__(self, num: int = 1):
        super().__init__()

        self.addRequirements(robot.drivetrain)

        self.num = num

        robot.drivetrain.resetGyro()

    def initialize(self):
        robot.drivetrain.stop()
        robot.drivetrain.setProfile(0)

        self.lastY = None
        self.slowed = False

        with open(os.path.dirname(robot.__file__) + "/trajectorydata.txt", "w") as f:

            sys.stdout = f

            # print(self.num)

            f.close()

        self.standardOut = sys.stdout

    def execute(self):
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

        with open(os.path.dirname(robot.__file__) + "/trajectorydata.txt", "w") as f:

            sys.stdout = f

            print([robot.drivetrain.getSpeeds(), robot.drivetrain.getModuleAngles()])

            f.close()

    def end(self, interrupted):
        with open(os.path.dirname(robot.__file__) + "/trajectorydata.txt", "w") as f:

            sys.stdout = f

            print("|||")

            f.close()

        sys.stdout = self.standardOut
