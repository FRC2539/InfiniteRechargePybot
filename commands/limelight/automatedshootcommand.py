from commands2 import ParallelCommandGroup

import robot

from commands.shooter.shootingprocesscommand import ShootingProcessCommand

from commands.limelight.sudocommandgroup import SudoCommandGroup


class AutomatedShootCommand(ParallelCommandGroup):
    def __init__(self, rpm=4400, ballCount=-1):
        super().__init__()

        self.addCommands(
            SudoCommandGroup(), ShootingProcessCommand(rpm, ballCount=ballCount)
        )
