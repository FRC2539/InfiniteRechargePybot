from commands2 import CommandBase

from robotpy_ext.misc import NotifierDelay

import constants
import robot
from controller import logicalaxes
from custom import driverhud
import math, sys, os


logicalaxes.registerAxis("forward")
logicalaxes.registerAxis("strafe")
logicalaxes.registerAxis("rotate")


class RecordAutoCommand(CommandBase):
    def __init__(self):
        """
        Run this command by toggling it, moving the
        robot, and then toggling it off. When you toggle
        it off, the netconsole will contain an output
        with the points.
        """
        super().__init__()

        self.addRequirements(robot.drivetrain)

        self.points = []

        robot.drivetrain.resetGyro()

    def initialize(self):
        robot.drivetrain.stop()
        robot.drivetrain.setProfile(0)

        self.lastY = None
        self.slowed = False

    def execute(self):
        with NotifierDelay(0.01) as delay:
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

            print(robot.drivetrain.getSpeeds())

            self.points.append(
                [robot.drivetrain.getPercents(), robot.drivetrain.getModuleAngles()]
            )

            delay.wait()

    def end(self, interrupted):
        robot.drivetrain.stop()

        print("\n\nPoints: [[flv, frv, blv, brv], [fla, fra, bla, bra]]")  # lol
        print("----------------------------------------------------")
        for line in self.points:
            print(line)
        print("----------------------------------------------------")
        print("Compact Form: " + str(self.points) + "\n")
        constants.drivetrain.mostRecentPath = self.points
        print("Exported to constants\n\n")
