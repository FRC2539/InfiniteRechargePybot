from commands2 import ParallelCommandGroup
import commandbased.flowcontrol as fc

import robot

from .drivetrain.resettiltcommand import ResetTiltCommand


class StartUpCommandGroup(ParallelCommandGroup):
    def __init__(self):
        super().__init__()
        
        t = ResetTiltCommand()
        
        self.addCommands(t)
        
    def runsWhenDisabled(self):
        return True