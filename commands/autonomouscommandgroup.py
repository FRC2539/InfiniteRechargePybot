from commands2 import SequentialCommandGroup, ParallelCommandGroup, CommandBase, InstantCommand, Swerve4ControllerCommand

from commands.drivetrain.turncommand import TurnCommand
from commands.drivetrain.movecommand import MoveCommand
from commands.drivetrain.curvecommand import CurveCommand
from commands.drivetrain.generatetrajectorycommand import GenerateTrajectoryCommand

from commands.intake.intakecommand import IntakeCommand

from commands.limelight.automatedshootcommand import AutomatedShootCommand

from wpilib.controller import PIDController, ProfiledPIDControllerRadians

from wpimath.trajectory import TrapezoidProfileRadians

import robot

class AutonomousCommandGroup(SequentialCommandGroup):
    def __init__(self):
        super().__init__()

        #self.intake = IntakeCommand()
        #self.move = MoveCommand(204)

        #self.toRun = self.move.alongWith(self.intake)

        #self.stopIntake = InstantCommand(robot.intake.dontIntakeBalls, [robot.intake])
        #self.moveBack = MoveCommand(-204)
        
        #self.sudo = AutomatedShootCommand()

        #self.addCommands(self.toRun,
                         #self.stopIntake,
                         #self.moveBack,
                         #self.sudo,
                         #)
                         