from wpilib import DriverStation

from commands2 import (
    SequentialCommandGroup,
    ParallelCommandGroup,
    CommandBase,
    InstantCommand,
    WaitCommand,
    Swerve4ControllerCommand,
)
from commands.drivetrain.cougarcoursecommand import CougarCourseCommand

from commands.drivetrain.turncommand import TurnCommand
from commands.drivetrain.turntocommand import TurnToCommand
from commands.drivetrain.movecommand import MoveCommand
from commands.drivetrain.generatevectors import GenerateVectors
from commands.drivetrain.pathfollowercommand import PathFollowerCommand
from commands.drivetrain.segmentfollowercommand import SegmentFollowerCommand
from commands.drivetrain.dosadocommand import DosadoCommand
from commands.drivetrain.bezierpathcommand import BezierPathCommand
from commands.drivetrain.trajectoryfollowercommand import TrajectoryFollowerCommand
from commands.hood.sethoodpositioncommand import SetHoodPositionCommand

from commands.limelight.automatedshootcommand import AutomatedShootCommand

from wpilib.controller import PIDController, ProfiledPIDControllerRadians

from wpimath.trajectory import (
    TrajectoryGenerator,
    TrajectoryConfig,
    TrapezoidProfileRadians,
)
from wpimath.geometry import Translation2d, Rotation2d, Pose2d

from networktables import NetworkTables

import math
import robot, constants

from commands import autoconfig


class AutonomousCommandGroup(SequentialCommandGroup):
    def __init__(self):
        super().__init__()

        ds = DriverStation.getInstance()
        msg = ds.getGameSpecificMessage()

        self.currentAuto = autoconfig.getAutoProgram()
        toRun = self.currentAuto

        for var in dir(self):  # Identifies the method to setup.
            if var.lower() == self.currentAuto:
                toRun = var
                break

        eval("self." + toRun + "()")  # Setups the method.

    def trajectoryTest(self):
        """
        Follow a basic trajectory.
        """
        
        self.addCommands(
            TrajectoryFollowerCommand(robot.drivetrain.trajectory)
        )

    def getOffTheLine(self):
        """
        Literally, just move 3.5 feet back off the line.
        """
        self.addCommands(MoveCommand(42))

    def shootFirstThree(self):
        """
        Shoots the first three balls, nothing more, nothing less.
        """
        self.addCommands(
            InstantCommand(lambda: robot.shooter.setRPM(3800), [robot.shooter]),
            MoveCommand(42),
            AutomatedShootCommand(3800, conveyorDelay=True),
        )

    def trenchSixBall(self):
        """
        Shoots three and pickups the other three, moves to a safer shooting location.
        """
        self.addCommands(
            InstantCommand(lambda: robot.shooter.setRPM(4100), [robot.shooter]),
            MoveCommand(48),
            InstantCommand(lambda: robot.pneumatics.extendIntake()),
            AutomatedShootCommand(4100, ballCount=3, conveyorDelay=True).withTimeout(4),
            InstantCommand(lambda: robot.shooter.setRPM(4100), [robot.shooter]),
            InstantCommand(
                lambda: robot.conveyorintake.move(0.7), [robot.conveyorintake]
            ),
            MoveCommand(120, torySlow=5200),
            MoveCommand(-135, angle=15),
            AutomatedShootCommand(4100, conveyorDelay=True),
        )

    def inProgressRendevousSixBall(self):
        """
        Shoots three, and then grabs the three balls on the north
        face of the rendevous point.
        """
        self.addCommands(
            AutomatedShootCommand(3300, ballCount=3, conveyorDelay=True).withTimeout(4),
            InstantCommand(lambda: robot.shooter.setRPM(3300), [robot.shooter]),
            InstantCommand(lambda: robot.pneumatics.extendIntake(), [robot.pneumatics]),
            InstantCommand(
                lambda: robot.conveyorintake.intakeBalls(), [robot.conveyorintake]
            ),
            MoveCommand(74),
            BezierPathCommand([[0, 50], [0, 0], [20, 0], [20, 50]], speed=0.3),
            BezierPathCommand([[30, 40], [0, 0]], speed=0.4),
            AutomatedShootCommand(3300, ballCount=3),
        )

    def stealFiveBall(self):
        """
        Steal two balls from the enemy trench, and then shoots all.
        """
        self.addCommands(
            InstantCommand(
                lambda: robot.pneumatics.extendIntake(), [robot.conveyorintake]
            ),
            InstantCommand(
                lambda: robot.conveyorintake.move(0.5), [robot.conveyorintake]
            ),
            MoveCommand(87, torySlow=5000),
            TurnCommand(37),
            MoveCommand(10, torySlow=4000),
            InstantCommand(lambda: robot.shooter.setRPM(3300), [robot.shooter]),
            MoveCommand(-145, angle=-20),
            InstantCommand(lambda: robot.conveyorintake.waitToRetract(), [robot.conveyorintake]),
            AutomatedShootCommand(3400, conveyorDelay=True),
        )

    def cougarCourseTest(self):
        CougarCourseCommand(
            [(0, 1), (1, 0), (0, -1)], graphAtSim=True, name="Test Path"
        )

    def inProgressEightBall(self):
        """
        Soon to be eight ball. Robot shoots 3 starting balls then collects 5 additional balls from the north face of the rendevous point and shoots them. Currently starts with 3 balls, goes around the pillar and shoots them from there.
        """
        self.addCommands(
            InstantCommand(lambda: robot.shooter.setRPM(4100), [robot.shooter]),
            InstantCommand(lambda: robot.pneumatics.extendIntake(), [robot.pneumatics]),
            AutomatedShootCommand(
                4100, ballCount=3, conveyorDelay=True, waitUntilAimed=True
            ).withTimeout(4),
            InstantCommand(
                lambda: robot.conveyorintake.move(0.7), [robot.conveyorintake]
            ),
            BezierPathCommand([[0, 0], [0, 140], [0, 150], [90, 150]], speed=0.75),
            InstantCommand(lambda: robot.shooter.setRPM(4100), [robot.shooter]),
            InstantCommand(lambda: robot.conveyorintake.stop(), [robot.conveyorintake]),
            TurnCommand(-15),
            AutomatedShootCommand(
                4100, ballcount=5, conveyorDelay=True, waitUntilAimed=True
            ),
            InstantCommand(
                lambda: robot.pneumatics.retractIntake(), [robot.pneumatics]
            ),
        )

    def interrupted(self):
        """
        Not an actual auto program.
        """
        robot.conveyorintake.stop()
        robot.chamber.stop()
        robot.shooter.stopShooter()

    def eightBall(self):
        """
        Shoot from the line, then collect 5 balls from the rendevous point and shoot those.

        Speeds are slow for testing purposes.
        """
        self.addCommands(
            # First 3 balls
            InstantCommand(lambda: robot.shooter.setRPM(2300), [robot.shooter]),
            InstantCommand(lambda: robot.pneumatics.extendIntake(), [robot.pneumatics]),
            AutomatedShootCommand(2250, ballCount=3, conveyorDelay=True).withTimeout(
                2.5
            ),
            InstantCommand(lambda: robot.pneumatics.extendIntake(), [robot.pneumatics]),
            # Curve to 4 balls
            MoveCommand(160, torySlow=28000),
            TurnCommand(98),
            InstantCommand(
                lambda: robot.conveyorintake.move(0.85), [robot.conveyorintake]
            ),
            # Intake 0.85
            MoveCommand(84, torySlow=3250),
            # Move 2750
            # InstantCommand(lambda: robot.conveyorintake.move(0.75), [robot.conveyorintake]),
            # MoveCommand(42, torySlow = 2000),
            InstantCommand(lambda: robot.shooter.setRPM(2800), [robot.shooter]),
            TurnCommand(149, tolerance=7),
            # Last ball
            InstantCommand(
                lambda: robot.conveyorintake.move(0.8), [robot.conveyorintake]
            ),
            # Intake 0.8
            MoveCommand(92, torySlow=18000),
            InstantCommand(
                lambda: robot.conveyorintake.outtakeBalls(), [robot.conveyorintake]
            ),
            InstantCommand(lambda: robot.shooter.setRPM(2300), [robot.shooter]),
            SetHoodPositionCommand(100),
            # Turn to shoot.
            TurnCommand(125),
            AutomatedShootCommand(3000, ballCount=5, conveyorDelay=True).withTimeout(6),
        )

    def pickupEightBall(self):
        """
        Experimental. Do not use this one in comp yet!
        """
        self.addCommands(
            # First 3 balls
            InstantCommand(lambda: robot.shooter.setRPM(2300), [robot.shooter]),
            InstantCommand(lambda: robot.pneumatics.extendIntake(), [robot.pneumatics]),
            AutomatedShootCommand(2250, ballCount=3, conveyorDelay=True).withTimeout(
                2.5
            ),
            InstantCommand(lambda: robot.pneumatics.extendIntake(), [robot.pneumatics]),
            # Curve to 4 balls
            MoveCommand(160, torySlow=28000),
            TurnCommand(98),
            InstantCommand(
                lambda: robot.conveyorintake.move(0.85), [robot.conveyorintake]
            ),
            # Intake 0.85
            MoveCommand(84, torySlow=3250),
            # Move 2750
            # InstantCommand(lambda: robot.conveyorintake.move(0.75), [robot.conveyorintake]),
            # MoveCommand(42, torySlow = 2000),
            InstantCommand(lambda: robot.shooter.setRPM(2800), [robot.shooter]),
            TurnCommand(149, tolerance=7),
            # Last ball
            InstantCommand(
                lambda: robot.conveyorintake.move(0.8), [robot.conveyorintake]
            ),
            # Intake 0.8
            MoveCommand(92, torySlow=18000),
            InstantCommand(
                lambda: robot.conveyorintake.outtakeBalls(), [robot.conveyorintake]
            ),
            InstantCommand(lambda: robot.shooter.setRPM(2300), [robot.shooter]),
            SetHoodPositionCommand(100),
            # Turn to shoot.
            TurnCommand(125),
            AutomatedShootCommand(3000, ballCount=5, conveyorDelay=True).withTimeout(6),
        )
