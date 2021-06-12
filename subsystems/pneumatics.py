from .cougarsystem import CougarSystem

import ports
import math
from wpilib import Compressor, DoubleSolenoid


class Pneumatics(CougarSystem):
    '''Describe what this subsystem does. (Nothing at the moment)'''

    def __init__(self):
        super().__init__("Pneumatics")
        
        self.compressor = Compressor(ports.pneumatics.pcmID)
        self.compressor.setClosedLoopControl(True)
        
        self.intakeSolenoid = DoubleSolenoid(ports.pneumatics.pcmID, ports.pneumatics.forwardChannel, ports.pneumatics.reverseChannel)
        
    def extendIntake(self):
        self.intakeSolenoid.set(Value.kForward)
        
    def retractIntake(self):
        self.intakeSolenoid.set(Value.kReverse)
    
    def toggleIntake(self):
        self.intakeSolenoid.toggle()
