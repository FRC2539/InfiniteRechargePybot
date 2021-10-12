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

        self.colorMatcher.addColorMatch(Color(0, 0.4, 0.4))  # Blue
        self.colorMatcher.addColorMatch(Color(0.7, 0, 0))  # Red
        self.colorMatcher.addColorMatch(Color(0.4, 0.4, 0))  # Yellow
        self.colorMatcher.addColorMatch(Color(0, 0.7, 0))  # Green

        # self.colors = ["y", "r", "g", "b", "y", "r", "g", "b"]

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

        self.controller.setP(0.001, 0)
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

    def getColor(self):
        # print(self.colorSensor.getColor())

        return self.colorMatcher.matchClosestColor(self.colorSensor.getColor(), 0.9)

    def getColorAsArray(self):
        currentColor = self.getColor()

        print([currentColor.red, currentColor.green, currentColor.blue])

        return [currentColor.red, currentColor.green, currentColor.blue]

    # def getColor(self):
    #     self.color = self.colorSensor.getColor()
    #     # print("r: " + str(self.color.red))
    #     # print("g: " + str(self.color.green))
    #     # print("b: " + str(self.color.blue))
    #     # print("ny: " + str(self.color.red / self.color.green))

    #     if (
    #         self.color.blue > (self.color.green - 0.18)
    #         and self.color.blue > self.color.red
    #     ):  # subtracts because there is more green in blue than blue lol.
    #         print("set b")
    #         return "b"
    #     # elif self.color.red > self.color.green and self.color.red > self.color.blue:
    #     #   return 'r'
    #     elif (
    #         self.color.green - 0.25 > self.color.red
    #         and self.color.green > self.color.blue
    #     ):
    #         # print("green")
    #         return "set g"
    #     elif (
    #         self.color.red / self.color.green < 0.65
    #     ):  # checks a highly-tuned ratio for current color since yellow isn't RGB and if you think it is you're an idiot.
    #         # print("yellow")
    #         return "set y"  # cough cough people who deleted Bens winch code cough cough
    #     else:
    #         # print("red")
    #         return "set r"

    # def getSensorColor(self):
    #     return self.sensor.getColor()
