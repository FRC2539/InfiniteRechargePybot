import ports

from rev import CANSparkMax, IdleMode, MotorType
from .cougarsystem import *


class Intake(CougarSystem):
    """Manages the intake of the robot."""

    # TODO: Program this subsystem so it is similar to the chamber's layout (younger kid)!

    def __init__(self):
        super().__init__("Intake")

        self.motor = CANSparkMax(ports.intake.motorID, MotorType.kBrushless)
        self.motor.setIdleMode(IdleMode.kBrake)
        self.motor.setInverted(True)
        self.motor.burnFlash()

        self.constantlyUpdate("Intake Running", (lambda: self.motor.get() != 0))

    def periodic(self):
        """
        Loops when nothing else is running in
        this subsystem. Do not call this!
        """
        self.feed()

    def intakeBalls(self, speed=0.65):
        """
        Runs the intake so that it intakes balls.
        """
        self.motor.set(speed)

    def fastOut(self):
        """
        Reverses the intake so it spits balls back out
        rather quickly.
        """
        self.motor.set(-0.5)

    def slowIn(self):
        """
        Intake balls slowly.
        """
        self.motor.set(0.4)

    def slowOut(self):
        """
        Reverses the intake motor so it slowly returns
        balls.
        """
        self.motor.set(-0.25)

    def dontIntakeBalls(self):
        """
        Kieren's way of naming the stop intake motor
        method lol.
        """
        self.motor.stopMotor()
