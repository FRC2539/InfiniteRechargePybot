from .cougarsystem import *

from wpilib import AnalogInput

import ports

from ctre import WPI_TalonSRX, NeutralMode, ControlMode


class Chamber(CougarSystem):
    """
    Controls the chamber in the ball system.
    The chamber moves the balls vertically and preceeds the shooter.
    """

    def __init__(self):
        super().__init__("Chamber")

        self.motor = WPI_TalonSRX(ports.chamber.motorID)

        self.motor.setNeutralMode(NeutralMode.Brake)
        self.motor.setInverted(True)

        # INFO: Percentages are from 0 - 1, 1 being 100%
        self.speed = 1.0  # 0.8
        self.slowSpeed = 0.2
        # Option: separate into forward and backward speeds

        # The sensor for telling if a ball is present.
        self.ballSensor = AnalogInput(ports.chamber.sensorPort)

        # Constantly updates the chamber's status.
        self.constantlyUpdate(
            "Chamber Running", lambda: self.motor.getMotorOutputPercent() != 0
        )

    def periodic(self):
        """
        Loops when nothing else is running in
        this subsystem. Do not call this!
        """
        self.feed()

    def forward(self):
        """
        Run the chamber so the balls move
        forwards.
        """
        self.move(self.speed)

    def backward(self):
        """
        Reverse the chamber so the balls
        move backwards.
        """
        self.move(-self.speed)

    def slowForward(self):
        """
        Run the chamber slowly so the balls
        move forward.
        """
        self.move(self.slowSpeed)

    def slowBackward(self):
        """
        Run the chamber slowly so the balls
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
        Stops the chamber motor.
        """
        self.motor.stopMotor()

    def isBallPresent(self):
        """
        Does the ball sensor see a ball?
        """
        return self.ballSensor.getValue() < 50
