from commands2 import SequentialCommandGroup, ParallelCommandGroup, CommandBase

from commands.drivetrain.turncommand import TurnCommand
from commands.drivetrain.movecommand import MoveCommand
from commands.drivetrain.curvecommand import CurveCommand

from commands.intake.intakecommand import IntakeCommand

from commands.chamber.chamberforwardcommand import ChamberForwardCommand

import robot

class AutonomousCommandGroup(SequentialCommandGroup):
    def __init__(self):
        super().__init__()

        intake = ChamberForwardCommand()
        move = MoveCommand(204)

        toRun = move.alongWith(intake)

        self.addCommands(toRun)
