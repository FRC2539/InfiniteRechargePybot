from .cougarsystem import *

import ports
import wpilib
import math

from wpilib import Color

from rev import CANSparkMax, MotorType, ControlType, IdleMode
from rev.color import ColorSensorV3, ColorMatch


class ColorWheel(CougarSystem):
    """Controls the color wheel spinner."""

    def __init__(self):
        super().__init__("ColorWheel")

        self.colorMatcher = ColorMatch()

        self.colorMatcher.addColorMatch(Color(0.15, 0.43, 0.42))  # Blue
        self.colorMatcher.addColorMatch(Color(0.51, 0.35, 0.14))  # Red
        self.colorMatcher.addColorMatch(Color(0.33, 0.55, 0.13))  # Yellow
        self.colorMatcher.addColorMatch(Color(0.18, 0.57, 0.25))  # Green

        self.colorSensor = ColorSensorV3(wpilib.I2C.Port.kOnboard)

        self.colorSensor.configureColorSensor(
            ColorSensorV3.ColorResolution.k18bit,
            ColorSensorV3.ColorMeasurementRate.k50ms,
        )

        self.motor = CANSparkMax(ports.colorWheelSpinner.motor, MotorType.kBrushless)
        self.motor.setIdleMode(IdleMode.kBrake)
        self.motor.setInverted(False)

        self.encoder = self.motor.getEncoder()
        self.controller = self.motor.getPIDController()

        self.controller.setP(0.01, 0)
        self.controller.setI(0, 0)
        self.controller.setD(0, 0)
        self.controller.setFF(0, 0)
        self.controller.setIZone(0, 0)

        self.speed = 0.2

        self.constantlyUpdate("Spinner Position", self.getPosition)
        self.constantlyUpdate("Color", self.getColorAsArray)

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

    def spinRotations(self, rotations):
        self.controller.setReference(rotations, ControlType.kPosition)

    def getColor(self):
        return self.colorMatcher.matchClosestColor(self.colorSensor.getColor(), 0.9)

    def getColorAsArray(self):
        currentColor = self.getColor()

        # print([currentColor.red, currentColor.green, currentColor.blue])

        return [currentColor.red, currentColor.green, currentColor.blue]
