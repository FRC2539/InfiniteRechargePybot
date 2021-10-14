from commands2 import CommandBase

import robot
import math
import constants


class RotationControlCommand(CommandBase):
    def __init__(self, rotations=4):
        super().__init__()

        self.addRequirements(robot.colorwheel)

        self.rotations = rotations

    def initialize(self):
        self.initialPosition = robot.colorwheel.getPosition()

        controlPanelCircumference = math.pi * constants.colorWheel.controlPanelDiameter
        spinnerCircumference = math.pi * constants.colorWheel.spinnerDiameter

        rotationsPerPanelRotation = controlPanelCircumference / spinnerCircumference

        self.rotationsNeeded = self.rotations * rotationsPerPanelRotation

        print(self.rotationsNeeded)

        robot.colorwheel.spinRotations(self.initialPosition + self.rotationsNeeded)

    def isFinished(self):
        currentPosition = robot.colorwheel.getPosition()

        return currentPosition - self.initialPosition >= self.rotationsNeeded

    def end(self, interrupted):
        robot.colorwheel.stopSpinner()
