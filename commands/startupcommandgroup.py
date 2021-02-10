from commands2 import CommandGroupBase
import commandbased.flowcontrol as fc

import robot

from .drivetrain.resettiltcommand import ResetTiltCommand


class StartUpCommandGroup(CommandGroupBase):
    def __init__(self):
        super().__init__()
        self.setRunWhenDisabled(True)

        self.addParallel(ResetTiltCommand())
