from .cougarsystem import *

from ctre import WPI_TalonSRX, FeedbackDevice, ControlMode, NeutralMode

import ports

# May need these
import robot
import math


class Turret(CougarSystem):
    """Controls the turret."""

    def __init__(self):
        super().__init__("Turret")

        self.motor = WPI_TalonSRX(ports.turret.motorID)
        self.motor.config_kP(0, 3.9, 0)
        self.motor.config_kI(0, 0, 0)
        self.motor.config_kD(0, 30, 0)
        self.motor.config_kF(0, 0.07, 0)

        self.maxPosition = 13
        self.minPosition = -13

        self.motor.setNeutralMode(NeutralMode.Brake)

        self.motor.configSelectedFeedbackSensor(FeedbackDevice.QuadEncoder, 0, 0)

        self.motor.setSelectedSensorPosition(0, 0, 0)

    def move(self, speed):
        if self.positionIsInBounds():
            self.motor.set(speed)

    def positionIsInBounds(self):
        return self.minPosition <= self.getPosition() <= self.maxPosition

    def getPosition(self):
        return self.motor.getSelectedSensorPosition(0)

    def stop(self):
        self.motor.stopMotor()


    def initDefaultCommand(self):
        from commands.turret.defaultcommand import DefaultCommand

        self.setDefaultCommand(DefaultCommand())
