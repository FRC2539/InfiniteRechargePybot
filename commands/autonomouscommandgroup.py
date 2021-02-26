from commands2 import SequentialCommandGroup, ParallelCommandGroup, CommandBase, InstantCommand

from commands.drivetrain.turncommand import TurnCommand
from commands.drivetrain.movecommand import MoveCommand
from commands.drivetrain.curvecommand import CurveCommand

from commands.intake.intakecommand import IntakeCommand

import robot

class AutonomousCommandGroup(SequentialCommandGroup):
    def __init__(self):
        super().__init__()

        self.intake = IntakeCommand()
        self.move = MoveCommand(204)

        self.toRun = self.move.alongWith(self.intake)

        self.stopIntake = InstantCommand(robot.intake.dontIntakeBalls, [robot.intake])
        self.moveBack = MoveCommand(-204)

        self.addCommands(self.toRun,
                         #self.moveBack.beforeStarting(self.stopIntake, [robot.intake])
                         )
