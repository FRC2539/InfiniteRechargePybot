from .cougarsystem import *

import ports
import wpilib
import math

from rev import CANSparkMax, MotorType, ControlType, IdleMode
from rev.color import ColorSensorV3


class ColorWheel(CougarSystem):
    """Controls the color wheel spinner."""

    def __init__(self):
        super().__init__("ColorWheel")

        self.motor = CANSparkMax(ports.colorWheelSpinner.motor, MotorType.kBrushless)
        self.motor.setIdleMode(IdleMode.kBrake)
        self.motor.setInverted(False)

        self.encoder = self.motor.getEncoder()
        self.controller = self.motor.getPIDController()

        self.controller.setP(0.001, 0)
        self.controller.setI(0, 0)
        self.controller.setD(0, 0)
        self.controller.setFF(0, 0)
        self.controller.setIZone(0, 0)

        # self.sensor = ColorSensorV3(ports.colorWheelSpinner.sensor)

        self.speed = 0.2

        self.constantlyUpdate("Spinner Position", self.getPosition)
        # self.constantlyUpdate("Color", self.getSensorColor)

    def periodic(self):
        """
        Loops when nothing else is running in
        this subsystem. Do not call this!
        """
        self.feed()

    def getPosition(self):
        return self.encoder.getPosition()

    def stopSpinner(self):
        self.motor.stopMotor()

    def setPercent(self, speed):
        self.motor.set(speed)

    def spin(self):
        self.setPercent(self.speed)

    def spinBackwards(self):
        self.setPercent(-self.speed)

    # def getSensorColor(self):
    #     return self.sensor.getColor()
