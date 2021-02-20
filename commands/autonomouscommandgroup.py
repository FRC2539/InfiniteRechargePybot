from commands2 import SequentialCommandGroup

from commands.drivetrain.turncommand import TurnCommand
from commands.drivetrain.movecommand import MoveCommand


class AutonomousCommandGroup(SequentialCommandGroup):
    def __init__(self):
        super().__init__()

        self.addCommands(TurnCommand(90))
