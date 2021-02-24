from commands2 import SequentialCommandGroup
from commands2 import ParallelCommandGroup

from commands.drivetrain.turncommand import TurnCommand
from commands.drivetrain.movecommand import MoveCommand
from commands.drivetrain.curvecommand import CurveCommand

from commands.intake.intakecommand import IntakeCommand

import robot

class AutonomousCommandGroup(SequentialCommandGroup):
    def __init__(self):
        super().__init__()


        self.addCommands(
            IntakeCommand().alongWith(MoveCommand(204))
            )
