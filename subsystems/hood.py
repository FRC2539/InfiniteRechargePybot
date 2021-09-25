from .cougarsystem import *

import ports
import wpilib
import math

from rev import CANSparkMax, MotorType, ControlType, IdleMode


class Hood(CougarSystem):
    """Controls the shooter hood."""

    def __init__(self):
        super().__init__("Hood")

        self.motor = CANSparkMax(ports.hood.motorID, MotorType.kBrushless)
        self.motor.setIdleMode(IdleMode.kBrake)

        self.encoder = self.motor.getEncoder()
        self.controller = self.motor.getPIDController()

        self.controller.setP(0.001, 0)
        self.controller.setI(0, 0)
        self.controller.setD(0, 0)
        self.controller.setFF(0, 0)
        self.controller.setIZone(0, 0)

        self.tbEncoder = wpilib.DutyCycle(
            wpilib.DigitalInput(ports.hood.absoluteThroughbore)
        )

        self.speed = 0.3

        # Corrects for an inverted hood motor direction
        self.direction = -1

        self.angleMax = 327.00
        self.angleMin = 302.00

        self.constantlyUpdate("Hood Position", self.getPosition)

    def periodic(self):
        """
        Loops when nothing else is running in
        this subsystem. Do not call this!
        """
        self.feed()

    def getPosition(self):
        return self.tbEncoder.getOutput() * 360

    def stopHood(self):
        self.motor.stopMotor()

    def setPercent(self, speed):
        self.motor.set(speed * self.direction)

    def raiseHood(self):
        if self.isBelowMaxAngle():
            self.setPercent(self.speed)
        else:
            self.stopHood()

    def lowerHood(self):
        if self.isAboveMinAngle():
            self.setPercent(-self.speed)
        else:
            self.stopHood()

    def isAboveMinAngle(self):
        return self.angleMin < self.getPosition()

    def isBelowMaxAngle(self):
        return self.getPosition() < self.angleMax

    def isWithinBounds(self):
        return self.angleMin < self.getPosition() < self.angleMax
