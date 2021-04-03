from commands2 import ParallelCommandGroup

import robot

from commands.shooter.shootingprocesscommand import ShootingProcessCommand
from commands.shooter.setrpmcommand import SetRPMCommand

from commands.limelight.sudocommandgroup import SudoCommandGroup


class JustAimCommand(ParallelCommandGroup):
    def __init__(self, rpm=4300):
        super().__init__()

        self.addCommands(
            SetRPMCommand(rpm), SudoCommandGroup()
        )
