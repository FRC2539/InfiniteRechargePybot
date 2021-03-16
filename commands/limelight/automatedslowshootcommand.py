from commands2 import ParallelCommandGroup

import robot

from commands.shooter.slowshootingprocesscommand import SlowShootingProcessCommand

from commands.limelight.sudocommandgroup import SudoCommandGroup


class AutomatedSlowShootCommand(ParallelCommandGroup):
    def __init__(self, rpm=3800):
        super().__init__()

        self.addCommands(
            SudoCommandGroup(), SlowShootingProcessCommand(rpm)
        )
