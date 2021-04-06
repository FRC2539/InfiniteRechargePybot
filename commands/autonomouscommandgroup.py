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

from commands.intake.intakecommand import IntakeCommand

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

        self.Test()

    # eval("self." + toRun + "()")  # Setups the method.

    def tenBall(self):

        self.spinUp = InstantCommand(
            lambda: robot.shooter.setRPM(3800), [robot.shooter]
        )
        self.spinUpTwo = InstantCommand(
            lambda: robot.shooter.setRPM(3800), [robot.shooter]
        )
        self.grabBalls = InstantCommand(
            lambda: robot.intake.intakeBalls(), [robot.intake]
        )
        self.stopGrabbing = InstantCommand(
            lambda: robot.intake.dontIntakeBalls, [robot.intake]
        )
        self.conveyorRun = InstantCommand(
            lambda: robot.conveyor.forward(), [robot.conveyor]
        )

        self.moveForward = MoveCommand(124)
        self.secondMove = MoveCommand(112, angle=2)
        self.moveBack = MoveCommand(-24, angle=-1.5)
        self.turnToTarget = TurnCommand(-20)

        self.shoot = AutomatedShootCommand(3800).withTimeout(3.25)
        self.shootTwo = AutomatedShootCommand(3800)

        # Schedule the autonomous command
        self.auton = PathFollowerCommand().get(
            [[3.586, -4.228], [4.519, -3.042], [3.485, -2.159], [2.375, -3.224]],
            [3.6, -4.228, 0]
            #'/home/lvuser/py/Slalmon.wpilib.json'
            # working 10 ball
            # [[-120, -12], [-177, -67]],
            # [-124, -70, math.pi],
        )  # .withTimeout(3.5) # driverhud.getAutonomousProgram()

        self.addCommands(
            # self.spinUp,      # ~
            # self.grabBalls,   # ~ All total to
            # self.conveyorRun, # ~ 3 seconds ideally
            # self.moveForward, # ~
            # self.shoot,
            # self.secondMove,
            # self.spinUpTwo,      # - about 3 seconds, assuming up to speed.
            # self.conveyorRun,
            self.auton,  # 5 seconds
            # self.moveBack,
            # self.turnToTarget,
            # self.shootTwo        # 4 seconds
        )

    def Test(self):
        self.addCommands(
            BezierPathCommand([[0,60],[0,30],[30,30],[30,0]], speed=0.5)
        )

    def Slalom(self):
        self.addCommands(
            SegmentFollowerCommand(
                [
                    [0, 13],
                    [-28, 14],
                    [-64, 26],
                    [-64, 64],
                    [-63, 180],
                    [-10, 188, {'speed':0.9}],
                    [42, 192, {'speed':0.9}],
                    [49, 218, {'speed':0.9}],
                    [48, 258, {'speed':0.9}],
                    [8, 274, {'speed':0.9}],
                    [-40, 233, {'speed':0.9}],
                    [-40, 197, {'speed':0.9}],
                    [32, 194],
                    [32, 26, {'speed':0.9}],
                    [-64, 30, {'speed':0.9}],
                    [-66, -45, {'speed':0.9}],
                ],
                maxSpeed=1.6,
            ),
        )

    def BarellRacing(self):
        self.addCommands(
            SegmentFollowerCommand([[0, 116]], maxSpeed=1.3, stopWhenDone=True),
            SegmentFollowerCommand([[24, 0]], maxSpeed=1.3, stopWhenDone=False),
            DosadoCommand(
                36,
                startAngle=90,
                angleToTravel=280,
                maxSpeed=1,
                stopWhenDone=False,
                waitForAlign=True,
            ),
            SegmentFollowerCommand(
                [[0, 76]],
                maxSpeed=1.3,
                stopWhenDone=False,
                kP=0.04,
            ),
            DosadoCommand(
                36,
                startAngle=180,
                angleToTravel=-270,
                reverseStrafe=True,
                stopWhenDone=False,
            ),
            SegmentFollowerCommand(
                [[36, 0], [74, 100], [74, 112]],
                maxSpeed=1.2,
            ),
            DosadoCommand(
                44,
                startAngle=180,
                angleToTravel=180,
                reverseStrafe=True,
                waitForAlign=True,
            ),
            SegmentFollowerCommand([[-14, -246]], maxSpeed=1.5),
        )

    def Bounce(self):
        self.addCommands(
            SegmentFollowerCommand([[0, 38]], maxSpeed=1, stopWhenDone=True),
            SegmentFollowerCommand([[-44, 0]], maxSpeed=1, stopWhenDone=True),
            SegmentFollowerCommand([[52, 0]], maxSpeed=0.8, stopWhenDone=True),
            SegmentFollowerCommand([[0, 25]], maxSpeed=0.8, stopWhenDone=True),
            InstantCommand(lambda: robot.drivetrain.stop(), [robot.drivetrain]),
            InstantCommand(lambda: robot.drivetrain.waitForRoll(), [robot.drivetrain]),
            SegmentFollowerCommand([[18, 0]], maxSpeed=1, sideWaysAdjust=True, stopWhenDone=False),
            DosadoCommand(
                35,
                startAngle=90,
                angleToTravel=190,
                endAngle=-90,
                reverseForward=True,
                stopWhenDone=True,
                maxSpeed=1.25,
            ),
            SegmentFollowerCommand([[-82, -2]], maxSpeed=1.3, kP=0.03, sideWaysAdjust=True, stopWhenDone=True),
            InstantCommand(lambda: robot.drivetrain.stop(), [robot.drivetrain]),
            InstantCommand(lambda: robot.drivetrain.waitForRoll(), [robot.drivetrain]),
            SegmentFollowerCommand(
                [[87, -2]], maxSpeed=1.4, kP=0.03, sideWaysAdjust=True, stopWhenDone=True
            ),
            DosadoCommand(
                52,
                startAngle=90,
                angleToTravel=190,
                endAngle=-90,
                reverseForward=True,
                stopWhenDone=True,
                maxSpeed=1.35,
            ),
            SegmentFollowerCommand([[-85, 1]], maxSpeed=1.45, rearBonus=-0.2),
            InstantCommand(lambda: robot.drivetrain.stop(), [robot.drivetrain]),
            InstantCommand(lambda: robot.drivetrain.waitForRoll(), [robot.drivetrain]),
            SegmentFollowerCommand([[30, -1], [30, 40]], maxSpeed=1.5),
        )

    def GalacticSearchRedA(self):
        self.addCommands(
            InstantCommand(lambda: robot.intake.intakeBalls(0.8), [robot.intake]),
            WaitCommand(0.4),
            SegmentFollowerCommand(
                [
                    [0, 5, {"speed": 0.25}],
                    [0, 10, {"speed": 0.9}],
                    [30, 62, {"speed": 0.9}],
                    [-80, 60, {"speed": 1.3}],
                    [-80, 70, {"speed": 2.8}],
                    [-50, 300],
                ],
                maxSpeed=1.4,
            ),
        )

    def GalacticSearchRedB(self):
        self.addCommands(
            InstantCommand(lambda: robot.intake.intakeBalls(0.9), [robot.intake]),
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

    def interrupted(self):
        robot.intake.dontIntakeBalls()
        robot.chamber.stop()
        robot.conveyor.stop()
        robot.shooter.stopShooter()
