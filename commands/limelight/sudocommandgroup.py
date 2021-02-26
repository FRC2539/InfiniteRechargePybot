from commands2 import ParallelCommandGroup

from commands.turret.turretlimelightcommand import TurretLimelightCommand
from commands.hood.hoodlimelightcommand import HoodLimelightCommand

class SudoCommandGroup(ParallelCommandGroup):
    """Aims towards the target with the limelight."""
    def __init__(self):
        super().__init__()
        
        self.addCommands(TurretLimelightCommand(),
                          HoodLimelightCommand())
        
        
