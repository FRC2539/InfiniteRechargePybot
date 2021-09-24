from commands2 import ParallelCommandGroup

from commands.limelight.aimwithlimelightcommand import AimWithLimelightCommand
from commands.shooter.spinupandshootcommand import SpinUpAndShootCommand


class AutomatedShootCommand(ParallelCommandGroup):
    """
    Aims the robot towards the target,
    while speeding up the shooter and shooting
    """

    def __init__(self, rpm):
        super().__init__()

        self.addCommands(AimWithLimelightCommand(), SpinUpAndShootCommand(rpm))
