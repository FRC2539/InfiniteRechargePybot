from commands2 import ParallelCommandGroup
import commandbased.flowcontrol as fc

import robot

from .drivetrain.resettiltcommand import ResetTiltCommand


class StartUpCommandGroup(ParallelCommandGroup):
    def __init__(self):
        super().__init__()

        robot.drivetrain.initDefaultCommand()
        robot.turret.initDefaultCommand()
        robot.shooter.initDefaultCommand()

        self.addCommands(ResetTiltCommand())

    def runsWhenDisabled(self):
        return True
