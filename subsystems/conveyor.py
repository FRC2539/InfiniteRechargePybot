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
        self.speed = 0.8
        self.slowSpeed = 0.2
        # Option: separate into forward and backward speeds

        # Constantly updates the conveyor's status.
        self.constantlyUpdate(
            "Conveyor Running", lambda: self.motor.getMotorOutputPercent() != 0
        )

    def periodic(self):
        """
        Loops when nothing else is running in
        this subsystem. Do not call this!
        """
        self.feed()

    def forward(self):
        """
        Run the conveyor so the balls move
        forwards.
        """
        self.move(self.speed)

    def backward(self):
        """
        Reverse the conveyor so the balls
        move backwards.
        """
        self.move(-self.speed)

    def slowForward(self):
        """
        Run the conveyor slowly so the balls
        move forward.
        """
        self.move(self.slowSpeed)

    def slowBackward(self):
        """
        Run the conveyor slowly so the balls
        move backwards.
        """
        self.move(-self.slowSpeed)

    def move(self, speed):
        """
        Basic move method to set custom speed to the motor.
        """
        self.motor.set(ControlMode.PercentOutput, speed)

    def stop(self):
        """
        Stops the conveyor motor.
        """
        self.motor.stopMotor()
