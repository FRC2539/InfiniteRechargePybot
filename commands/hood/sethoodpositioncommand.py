from commands2 import CommandBase

import robot

import math


class SetHoodPositionCommand(CommandBase):
    def __init__(self, targetPosition):
        super().__init__()

        self.addRequirements(robot.hood)

        self.targetPosition = targetPosition

        self.positionIsValid = robot.hood.angleIsWithinBounds(targetPosition)

        self.maximumAdjustment = 0.1

        self.errorPercent = 0.05

        self.threshold = 0.5

    def execute(self):
        if not self.positionIsValid:
            pass

        positionError = self.targetPosition - robot.hood.getPosition()

        if abs(positionError) <= self.threshold:
            pass

        adjustment = math.copysign(
            max(self.maximumAdjustment, abs(positionError * self.errorPercent)),
            positionError,
        )

        robot.hood.setPercent(adjustment)

    def isFinished(self):
        positionError = self.targetPosition - robot.hood.getPosition()

        return not self.positionIsValid or abs(positionError) <= self.threshold

    def end(self, interrupted):
        robot.hood.stop()
