from wpilib import DriverStation

from commands2 import (
    SequentialCommandGroup,
    ParallelCommandGroup,
    CommandBase,
    InstantCommand,
    WaitCommand,
    Swerve4ControllerCommand,
)

from commands.drivetrain.turncommand import TurnCommand
from commands.drivetrain.movecommand import MoveCommand
from commands.drivetrain.generatevectors import GenerateVectors
from commands.drivetrain.pathfollowercommand import PathFollowerCommand
from commands.drivetrain.cougarcoursecommand import CougarCourseCommand
from commands.drivetrain.runautocommand import RunAutoCommand
from commands.drivetrain.segmentfollowercommand import SegmentFollowerCommand
from commands.drivetrain.dosadocommand import DosadoCommand
from commands.drivetrain.bezierpathcommand import BezierPathCommand

from commands.limelight.automatedshootcommand import AutomatedShootCommand

from wpilib.controller import PIDController, ProfiledPIDControllerRadians

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

    def Slalom(self):
        """
        IR@H Challenge.
        """

        # NOTE: Don't write autos like this, for the love of God.

        self.addCommands(
            SegmentFollowerCommand(
                [
                    [0, 13],
                    [-28, 14],
                    [-64, 26],
                    [-64, 64],
                    [-63, 180],
                    [-10, 188, {"speed": 0.9}],
                    [42, 192, {"speed": 0.9}],
                    [49, 218, {"speed": 0.9}],
                    [48, 258, {"speed": 0.9}],
                    [8, 274, {"speed": 0.9}],
                    [-40, 233, {"speed": 0.9}],
                    [-40, 197, {"speed": 0.9}],
                    [32, 194],
                    [32, 26, {"speed": 0.9}],
                    [-64, 30, {"speed": 0.9}],
                    [-66, -45, {"speed": 0.9}],
                ],
                maxSpeed=1.6,
            ),
        )

    def BarrelRacing(self):
        """
        IR@H Challenge.
        """
        self.addCommands(
            BezierPathCommand(
                [[0, 0], [70, 30], [75, 0]], speed=1.4, stopWhenDone=False
            ),
            BezierPathCommand(
                [[90, 70], [90, 0], [10, 0], [10, 70]], speed=1.2, stopWhenDone=False
            ),
            BezierPathCommand(
                [[0, 20], [10, 60], [195, 10], [195, 80]], speed=1.2, stopWhenDone=False
            ),
            BezierPathCommand(
                [[90, 10], [90, 80], [0, 80], [0, 10]], speed=1.1, stopWhenDone=False
            ),
            BezierPathCommand(
                [[0, 110], [0, 30], [10, 0], [70, 0]], speed=1.25, stopWhenDone=False
            ),
            BezierPathCommand(
                [[0, 0], [115, 0], [115, 45], [50, 60]], speed=1.25, stopWhenDone=False
            ),
            BezierPathCommand([[250, 0], [210, 5], [0, 7]], speed=1.5),
        )

    def Bounce(self):
        """
        IR@H Challenge.
        """
        self.addCommands(
            BezierPathCommand([[0, 0], [40, 0], [38, 45]], speed=1),
            InstantCommand(lambda: robot.drivetrain.stop(), [robot.drivetrain]),
            InstantCommand(lambda: robot.drivetrain.waitForRoll(), [robot.drivetrain]),
            BezierPathCommand(
                [[0, 100], [0, 0], [20, 40], [20, 0]], speed=1, stopWhenDone=False
            ),
            BezierPathCommand(
                [[0, 90], [0, 50], [56, 50], [56, 90]], speed=1, stopWhenDone=False
            ),
            BezierPathCommand([[0, 0], [0, 90], [0, 90]], speed=1),
            InstantCommand(lambda: robot.drivetrain.stop(), [robot.drivetrain]),
            InstantCommand(lambda: robot.drivetrain.waitForRoll(), [robot.drivetrain]),
            BezierPathCommand([[0, 90], [0, 0]], speed=1, stopWhenDone=False),
            BezierPathCommand(
                [[0, 54], [0, 0], [103, 0], [103, 54]], speed=1, stopWhenDone=False
            ),
            BezierPathCommand([[0, 0], [0, 78], [0, 78]], speed=1),
            InstantCommand(lambda: robot.drivetrain.stop(), [robot.drivetrain]),
            InstantCommand(lambda: robot.drivetrain.waitForRoll(), [robot.drivetrain]),
            BezierPathCommand([[0, 30], [0, 0], [15, 0]], speed=1),
        )

    def GalacticSearchRedA(self):
        """
        IR@H Challenge.
        """
        self.addCommands(
            InstantCommand(
                lambda: robot.conveyorintake.intakeBalls(), [robot.conveyorintake]
            ),
            WaitCommand(0.2),
            BezierPathCommand(
                [[200, 0], [190, 125], [209, 30], [209, 120]],
                speed=1.3,
                stopWhenDone=True,
            ),
            BezierPathCommand(
                [[160, 50], [7, 0], [37, 0], [57, 140]], speed=1.8, stopWhenDone=False
            ),
            BezierPathCommand([[0, 0], [0, 200]], speed=5),
        )

    def GalacticSearchRedB(self):
        """
        IR@H Challenge.
        """
        self.addCommands(
            InstantCommand(
                lambda: robot.conveyorintake.intakeBalls(), [robot.conveyorintake]
            ),
            WaitCommand(0.2),
            SegmentFollowerCommand(
                [
                    [0, 5, {"speed": 0.45}],
                    [0, 10, {"speed": 1.1}],
                    [50, 60, {"speed": 1.2}],
                    [-50, 130, {"speed": 3}],
                    [-25, 430],
                ]
            ),
        )

    def getOffTheLine(self):
        """
        Literally, just move 3.5 feet forward.
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
            MoveCommand(-135, angle=10),
            AutomatedShootCommand(4100, conveyorDelay=True),
        )

    def rendevousSixBall(self):
        """
        Shoots three, and then grabs the three balls on the north
        face of the rendevous point.
        """
        self.addCommands(
            AutomatedShootCommand(3300, ballCount=3, conveyorDelay=True).withTimeout(5),
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
            InstantCommand(lambda: robot.conveyorintake.stop(), [robot.conveyorintake]),
            AutomatedShootCommand(3300, conveyorDelay=True, waitUntilAimed=True),
        )

    def badEightBall(self):
        """
        Collects two additional balls from the trench, and then shoots all five.
        """

        self.addCommands(
            InstantCommand(lambda: robot.shooter.setRPM(3800), [robot.shooter]),
            MoveCommand(48, torySlow=26000),
            InstantCommand(lambda: robot.pneumatics.extendIntake()),
            AutomatedShootCommand(3800, ballCount=3, conveyorDelay=True).withTimeout(
                2.25
            ),
            InstantCommand(lambda: robot.shooter.setRPM(3800), [robot.shooter]),
            InstantCommand(
                lambda: robot.conveyorintake.move(0.7), [robot.conveyorintake]
            ),
            MoveCommand(120, torySlow=9000),
            MoveCommand(-100, angle=30, torySlow=28000),
            AutomatedShootCommand(4100, conveyorDelay=True).withTimeout(1.5),
            InstantCommand(lambda: robot.shooter.setRPM(3800), [robot.shooter]),
            TurnCommand(51),
            InstantCommand(
                lambda: robot.conveyorintake.move(0.6), [robot.conveyorintake]
            ),
            MoveCommand(26, torySlow=24000),
            MoveCommand(-20, torySlow=2800),
            TurnCommand(-51),
            AutomatedShootCommand(4100, conveyorDelay=True),
        )

    def bensEightBall(self):
        """
        Collects two additional balls from the trench, and then shoots all five.
        F in the chat bois. Didn't read the rules.
        """

        self.addCommands(
            InstantCommand(lambda: robot.shooter.setRPM(3800), [robot.shooter]),
            MoveCommand(48, torySlow=30000),
            InstantCommand(lambda: robot.pneumatics.extendIntake()),
            AutomatedShootCommand(3800, ballCount=3, conveyorDelay=True).withTimeout(
                2.75
            ),
            InstantCommand(lambda: robot.shooter.setRPM(3800), [robot.shooter]),
            InstantCommand(
                lambda: robot.conveyorintake.move(0.83), [robot.conveyorintake]
            ),
            BezierPathCommand([[0, 0], [0, 106]], speed=0.44, stopWhenDone=True),
            BezierPathCommand([[0, 108], [0, 12], [16, 10], [25, 9]], speed=1.4),
            InstantCommand(lambda: robot.conveyorintake.stop(), [robot.conveyorintake]),
            TurnCommand(44),
            InstantCommand(
                lambda: robot.conveyorintake.move(0.5), [robot.conveyorintake]
            ),
            MoveCommand(29, torySlow=22000),
            MoveCommand(-29, torySlow=30000),
            TurnCommand(-55),
            AutomatedShootCommand(3800, conveyorDelay=True),
        )

    def tenBall(self):
        # Needs to be rewritten. If you want to see it, view commits.
        pass

    def interrupted(self):
        """
        Not an actual auto program.
        """
        robot.conveyorintake.stop()
        robot.chamber.stop()
        robot.shooter.stopShooter()
