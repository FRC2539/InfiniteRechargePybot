from commands2 import ParallelCommandGroup

import robot

from commands.shooter.shootingprocesscommand import ShootingProcessCommand
from commands.shooter.shootingprocessvariablecommand import (
    ShootingProcessVariableCommand,
)

from commands.limelight.sudocommandgroup import SudoCommandGroup


class AutomatedShootCommand(ParallelCommandGroup):
    def __init__(self, rpm=4400, ballCount=-1, variableIntakeSpeed=None):
        super().__init__()
        if variableIntakeSpeed is None:
            self.addCommands(
                SudoCommandGroup(),
                ShootingProcessCommand(targetRPM=rpm, ballCount=ballCount),
            )
        else:
            self.addCommands(
                SudoCommandGroup(),
                ShootingProcessVariableCommand(
                    variableIntakeSpeed, targetRPM=rpm, ballCount=ballCount
                ),
            )
