from commands2 import CommandBase

from robotpy_ext.misc import NotifierDelay

import robot, constants

import math


class DosadoCommand(CommandBase):
    def __init__(
        self,
        radius,
        startAngle=90,
        angleToTravel=180,
        velocity=0.9,
        reverseStrafe=False,
        reverseForward=False,
        waitForAlign=False,
    ):
        """
        Note that startAngle is the module angles. The default is 90,
        which would be to the right of the robot's orientation. The angle
        to travel is how many degrees it should travel in total. Velocity is
        a percent of the max speed. counterclockwise describes how it should
        travel the circle. waitForAlign will wait for the wheels to align at
        the beginning if true.
        """
        super().__init__()

        self.addRequirements([robot.drivetrain])

        self.velPercent = velocity
        self.linearVelocity = velocity * constants.drivetrain.speedLimit
        self.radius = radius
        self.angle = startAngle
        self.angleToTravel = angleToTravel
        self.alterStrafe = reverseStrafe
        self.alterForward = reverseForward
        self.waitForAlign = waitForAlign

        if self.angle < 0:
            self.idToIndex = 0
        else:
            self.idToIndex = 1

        self.totalArcLength = (self.angleToTravel * math.pi / 180) * self.radius
        self.revPerSecond = self.linearVelocity / self.radius

    def initialize(self):
        robot.drivetrain.setModuleProfiles(
            1, drive=False
        )  # Use the secondary PIDs for the turn motor.
        self.startPos = robot.drivetrain.getPositions()[self.idToIndex]
        self.done = False

        robot.drivetrain.setUniformModuleAngle(self.angle)

        if self.waitForAlign:
            count = 0
            while (
                count <= 2
            ):  # Force the code to wait until we're aligned. WARNING: This can kill the code.
                count = 0
                for angle in robot.drivetrain.getModuleAngles():
                    if abs((angle % 180) - abs(self.angle)) < 5:
                        count += 1

    def execute(self):
        currentDistAlongArc = abs(
            robot.drivetrain.getPositions()[self.idToIndex] - self.startPos
        )
        if currentDistAlongArc >= abs(self.totalArcLength):
            self.done = True
        else:
            theta = currentDistAlongArc / self.radius  # The remaining angle.
            forward = (
                -self.revPerSecond
                * self.radius
                * math.cos(theta)
                / abs(self.linearVelocity)
            )
            strafe = (
                self.revPerSecond
                * self.radius
                * math.sin(theta)
                / abs(self.linearVelocity)
            )

            # Trust me, the evaluation SHOULD be opposite of what it changes.
            if self.alterForward:
                strafe = -strafe

            if self.alterStrafe:
                forward = -forward

            speeds, angles = robot.drivetrain._calculateSpeeds(strafe, forward, 0)

            speeds = [math.copysign(self.velPercent, speed) for speed in speeds]
            angles = [a - self.angle for a in angles]

            print("s " + str(speeds))

            robot.drivetrain.setSpeeds(speeds)
            robot.drivetrain.setModuleAngles(angles)

    def isFinished(self):
        return self.done

    def end(self, interrupted):
        robot.drivetrain.setModuleProfiles(0, drive=False)
