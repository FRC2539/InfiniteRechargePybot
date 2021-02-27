import ports

from rev import CANSparkMax, IdleMode, MotorType
from .cougarsystem import *

class Intake(CougarSystem):
    """Describe what this subsystem does."""

    def __init__(self):
        super().__init__('Intake')

        self.motor = CANSparkMax(ports.intake.motorID, MotorType.kBrushless)
        self.motor.setIdleMode(IdleMode.kBrake)
        self.motor.setInverted(True)
        self.motor.burnFlash()
                
        self.constantlyUpdate('Intake Running', (lambda: self.motor.get() != 0))
        
    def periodic(self):
        self.feed()
        
    def intakeBalls(self):
        self.motor.set(0.9)

    def fastOut(self):
        self.motor.set(-0.5)

    def slowIn(self):
        self.motor.set(0.4)

    def slowOut(self):
        self.motor.set(-0.25)

    def dontIntakeBalls(self):
        self.motor.stopMotor()

    def periodic(self):
        self.feed() # Required for the constant update.
