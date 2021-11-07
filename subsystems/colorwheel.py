from .cougarsystem import *

import ports
import wpilib
import math

from wpilib import Color

from rev import CANSparkMax, MotorType, ControlType, IdleMode
from rev.color import ColorSensorV3, ColorMatch

from networktables import NetworkTables


class ColorWheel(CougarSystem):
    """Controls the color wheel sensor."""

    def __init__(self):
        super().__init__("ColorWheel")

        self.fmsInfo = NetworkTables.getTable("FMSInfo")

        self.colorMatcher = ColorMatch()

        self.colors = [  # Colors in field order (important)
            Color(0.51, 0.35, 0.14),  # Red
            Color(0.33, 0.55, 0.13),  # Yellow
            Color(0.15, 0.43, 0.42),  # Blue
            Color(0.18, 0.57, 0.25),  # Green
        ]

        # Add all of the colors to the color match object
        for color in self.colors:
            self.colorMatcher.addColorMatch(color)

        self.colorSensor = ColorSensorV3(wpilib.I2C.Port.kOnboard)

        self.colorSensor.configureColorSensor(
            ColorSensorV3.ColorResolution.k18bit,
            ColorSensorV3.ColorMeasurementRate.k50ms,
        )

        self.constantlyUpdate("Color", self.getColorAsArray)

        self.put("Rotation Duration", 7)

        self.getNetworkTableValues()

    def getNetworkTableValues(self):
        self.rotationControlDuration = self.get("Rotation Duration", 7)

    def periodic(self):
        """
        Loops when nothing else is running in
        this subsystem. Do not call this!
        """
        self.feed()
        self.getNetworkTableValues()

    def getFieldColor(self):
        return self.fmsInfo.getValue("GameSpecificMessage", "R")

    def getColorsList(self):
        return self.colors

    def getColor(self):
        return self.colorMatcher.matchClosestColor(self.colorSensor.getColor(), 0.9)

    def getColorAsArray(self):
        currentColor = self.getColor()

        return [currentColor.red, currentColor.green, currentColor.blue]

    def getRotationDuration(self):
        return self.rotationControlDuration
