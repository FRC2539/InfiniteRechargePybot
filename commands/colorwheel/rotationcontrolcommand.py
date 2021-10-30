from commands2 import CommandBase

import robot


from commands2 import CommandBase

import robot
import math
import constants

from wpilib import Timer


class RotationControlCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.colorwheel, robot.chamber)

    def initialize(self):
        self.timer = Timer()

        self.timer.reset()
        self.timer.start()

        robot.chamber.spinColorWheel()

    def isFinished(self):
        return self.timer.hasElapsed(7.7)

    def end(self, interrupted):
        robot.chamber.stop()

        self.timer.stop()
