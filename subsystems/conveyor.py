from .cougarsystem import *

import ports

from ctre import WPI_TalonSRX, NeutralMode, ControlMode

class Conveyor(CougarSystem):
    """Controls the conveyor in the ball system. 
    The conveyor is horizontal and preceeds the chamber."""

    def __init__(self):
        super().__init__("Conveyor")

        self.motor = WPI_TalonSRX(ports.conveyor.motorID)

        self.motor.setNeutralMode(NeutralMode.Brake)
        self.motor.setInverted(True)

        # INFO: Percentages are from 0 - 1, 1 being 100%
        self.speed = 0.4
        self.slowSpeed = 0.2
        # Option: separate into forward and backward speeds

    def forward(self):
        move(self.speed)

    def backward(self):
        move(-self.speed)

    def slowForward(self):
        move(self.slowSpeed)

    def slowBackward(self):
        move(-self.slowSpeed)

    def move(self, speed):
        self.motor.set(ControlMode.PercentOutput, speed)

    def stop(self):
        self.motor.stopMotor()
