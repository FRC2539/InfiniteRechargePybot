from .cougarsystem import *

from ctre import WPI_TalonSRX, FeedbackDevice, ControlMode, NeutralMode

import ports

# May need these
import robot
import math


class Turret(CougarSystem):
    """Controls the robot's turret."""

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

        # Constantly updates the turret's status.
        self.constantlyUpdate(
            "Turret Moving", lambda: self.motor.getMotorOutputPercent() != 0
        )
        self.constantlyUpdate("Turret Position", self.getPosition)

    def periodic(self):
        """
        Loops when nothing else is running in
        this subsystem. Do not call this!
        """
        self.feed()

    def move(self, speed):
        """
        Safely move the turret. By safely,
        I mean it will not overrdrive by a large margin.
        """
        if (
            (speed > 0 and self.getPosition() >= self.minPosition)
            or (speed < 0 and self.getPosition() <= self.maxPosition)
            or self.positionIsInBounds()
        ):
            self.motor.set(speed)
        else:
            self.motor.stopMotor()

    def positionIsInBounds(self):
        """
        Is the turret in between the min and max position?
        Uses the encoder to check.
        """
        return self.minPosition <= self.getPosition() <= self.maxPosition

    def getPosition(self):
        """
        Returns the position of the turret's encoder in ticks.
        """
        return self.motor.getSelectedSensorPosition(0)

    def stop(self):
        """
        Stops the turret motor.
        """
        self.motor.stopMotor()

    def initDefaultCommand(self):
        """
        Establishes the default command to run. In this case,
        it is a command that allows us to turn the turret at anytime,
        assuming the turret is not in use elsewhere.
        """
        from commands.turret.defaultcommand import DefaultCommand

        self.setDefaultCommand(DefaultCommand())
