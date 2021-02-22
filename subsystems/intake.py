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
        
        self.intakeRunning = False
        
        self.put('Intake Running', self.intakeRunning)
        
    def intakeBalls(self):
        self.intakeRunning = True
        self.motor.set(0.5)

    def dontIntakeBalls(self):
        self.intakeBalls = False
        self.motor.stopMotor()

    def fastOut(self):
        self.intakeRunning = True
        self.motor.set(-0.5)
    
    def slowOut(self):
        self.intakeRunning = True
        self.motor.set(-0.25)

    def periodic(self):
        if self.hasChanged('Intake Running', self.intakeRunning):
            print('changed')
            self.put('Intake Running', self.intakeRunning)

    def slowOut(self):
        self.motor.set(-0.25)
