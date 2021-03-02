from .cougarsystem import *

import wpilib
import math
import ports

from rev import CANSparkMax, MotorType, ControlType, IdleMode
from custom.config import Config


class Hood(CougarSystem):
    """Controls the robot's shooter."""

    def __init__(self):
        super().__init__()

        self.encoder = wpilib.DutyCycle(wpilib.DigitalInput(ports.hood.encoderID))

        self.motor = CANSparkMax(ports.hood.motorID, MotorType.kBrushless)

        self.motor.setIdleMode(IdleMode.kBrake)

        self.motor.burnFlash()

        self.controller = self.motor.getPIDController()

        self.controller.setP(0.001, 0)
        self.controller.setI(0, 0)
        self.controller.setD(0, 0)
        self.controller.setFF(0, 0)
        self.controller.setIZone(0, 0)

        self.angleMax = 253.00
        self.angleMin = 220.00

        self.speed = 0.1  # 10 Percent

        # Constantly updates the hood's status.
        self.constantlyUpdate("Hood Moving", lambda: self.motor.get() != 0)
        self.constantlyUpdate("Hood Position", self.getPosition)

    def periodic(self):
        self.feed()

    def getPosition(self):
        return self.encoder.getOutput() * 360

    def up(self):
        self.move(self.speed)

    def down(self):
        self.move(-self.speed)

    def move(self, speed):
        if self.isInAngleBounds(speed):
            self.motor.set(speed)
        else:
            self.stop()

    def isInAngleBounds(self, speed=0):
        if speed > 0:
            return self.isUnderMaxAngle()
        elif speed < 0:
            return self.isAboveMinAngle()
        else:
            return self.isUnderMaxAngle() and self.isAboveMinAngle()

    def isUnderMaxAngle(self):
        return self.getPosition() <= self.angleMax

    def isAboveMinAngle(self):
        return self.angleMin <= self.getPosition()

    def stop(self):
        self.motor.stopMotor()
