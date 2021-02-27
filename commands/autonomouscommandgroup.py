from commands2 import SequentialCommandGroup, ParallelCommandGroup, CommandBase, InstantCommand

from commands2 import Swerve4ControllerCommand

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
        
        self.addCommands(
            Swerve4ControllerCommand(
                GenerateTrajectoryCommand(
                    [[1, 1], [2, -1]], [3, 0, 0]
                    ).getTrajectory(),
                robot.drivetrain.getSwervePose,
                robot.drivetrain.swerveKinematics,
                PIDController(0.1, 0, 0), # X-controller
                PIDController(0.1, 0, 0), # Y-controller
                ProfiledPIDControllerRadians(0.1, 0, 0, 
                    TrapezoidProfileRadians.Constraints(4, 2)
                                            ), # Theta-controller
                lambda: 0,
                robot.drivetrain.setModuleStates,
                [robot.drivetrain]
            )
        )