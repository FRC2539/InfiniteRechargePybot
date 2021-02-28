from commands2 import ParallelCommandGroup

import robot

from commands.shooter.shootingprocesscommand import ShootingProcessCommand
from commands.shooter.setrpmcommand import SetRPMCommand

from commands.limelight.sudocommandgroup import SudoCommandGroup


class AutomatedShootCommand(ParallelCommandGroup):
    def __init__(self, rpm=4000):
        super().__init__()

        self.addCommands(
            SetRPMCommand(rpm), SudoCommandGroup(), ShootingProcessCommand(rpm)
        )
