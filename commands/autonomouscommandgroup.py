from commands2 import (
    SequentialCommandGroup,
    ParallelCommandGroup,
    CommandBase,
    InstantCommand,
    Swerve4ControllerCommand,
)

from commands.drivetrain.turncommand import TurnCommand
from commands.drivetrain.movecommand import MoveCommand
from commands.drivetrain.curvecommand import CurveCommand

from commands.intake.intakecommand import IntakeCommand

from commands.limelight.automatedshootcommand import AutomatedShootCommand

from wpilib.controller import PIDController, ProfiledPIDControllerRadians

import robot


class AutonomousCommandGroup(SequentialCommandGroup):
    def __init__(self):
        super().__init__()

        self.conveyor = InstantCommand(robot.conveyor.forward, [robot.conveyor])

        self.turnBack = TurnCommand(20)
        self.realign = TurnCommand(-10)

        self.intake = InstantCommand(robot.intake.intakeBalls, [robot.intake])
        self.moveSide = MoveCommand(7.071, angle=45, slow=True)

        self.moveForward = MoveCommand(199, slow=True)

        self.stopIntake = InstantCommand(robot.intake.dontIntakeBalls, [robot.intake])
        self.moveBack = MoveCommand(-120, angle=14)

        self.sudo = AutomatedShootCommand(3000).withTimeout(4)
        self.sudoNT = AutomatedShootCommand()

        self.goBack = self.moveBack.alongWith(self.sudoNT)

        self.addCommands(
            # self.conveyor,
            self.sudo,
            self.turnBack,
            self.intake,
            self.moveSide,
            self.moveForward,
            self.realign,
            self.goBack,
        )

    def interrupted(self):
        robot.intake.dontIntakeBalls()
        robot.chamber.stop()
        robot.conveyor.stop()
        robot.shooter.stopShooter()
