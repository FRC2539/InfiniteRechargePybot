from .cougarsystem import CougarSystem

import ports
import math
import robot
from wpilib import Compressor, DoubleSolenoid


class Pneumatics(CougarSystem):
    """Describe what this subsystem does. (Nothing at the moment)"""

    def __init__(self):
        super().__init__("Pneumatics")

        self.compressor = Compressor(ports.pneumatics.pcmID)
        self.compressor.setClosedLoopControl(True)

        self.intakeSolenoid = DoubleSolenoid(
            ports.pneumatics.pcmID,
            ports.pneumatics.forwardChannel,
            ports.pneumatics.reverseChannel,
        )

    def extendIntake(self):
        robot.conveyorintake.resetWatchdog()
        self.intakeSolenoid.set(DoubleSolenoid.Value.kForward)

    def retractIntake(self):
        robot.conveyorintake.resetWatchdog()
        self.intakeSolenoid.set(DoubleSolenoid.Value.kReverse)

    def toggleIntake(self):
        self.intakeSolenoid.toggle()
