import ports

from rev import CANSparkMax, IdleMode, MotorType
from .cougarsystem import *


class Intake(CougarSystem):
    """Describe what this subsystem does."""

    def __init__(self):
        super().__init__()

        self.motor = CANSparkMax(ports.intake.motorID, MotorType.kBrushless)
        self.motor.setIdleMode(IdleMode.kBrake)
        self.motor.setInverted(True)
        self.motor.burnFlash()

    def intakeBalls(self):
        self.motor.set(0.5)

    def dontIntakeBalls(self):
        self.motor.stopMotor()

    def fastOut(self):
        self.motor.set(-0.5)

    def slowOut(self):
        self.motor.set(-0.25)
