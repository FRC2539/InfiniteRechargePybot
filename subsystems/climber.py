from .cougarsystem import CougarSystem

from ctre import WPI_TalonFX, NeutralMode

import ports
import math


class Climber(CougarSystem):
    '''Describe what this subsystem does.'''

    def __init__(self):
        super().__init__('Climber')
        
        # The motor and it's modifications. 
        self.climberMotor = WPI_TalonFX(ports.climber.motorID)
        
        self.climberMotor.setNeutralMode(NeutralMode.Brake)
        self.climberMotor.setSafetyEnabled(False)
        self.climberMotor.setInverted(False)
        
        # Standard speed of the climber, up and down.
        self.speed = 0.3
        
    def periodic(self):
        """
        Loops when nothing else is running in
        this subsystem. Do not call this!
        """
        self.feed()
        
    def raiseClimber(self):
        """
        Raises the climber using the climber motor.
        """
        self.climberMotor.set(self.speed)
        
    def lowerClimber(self):
        """
        Lowers the climber using the climber motor.
        """
        self.climberMotor.set(-self.speed)
        
    def stopClimber(self):
        """
        Stops the climber motor.
        """
        self.climberMotor.stopMotor()