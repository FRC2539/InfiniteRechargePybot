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
            BezierPathCommand([[40,-40], [-40,-40], [-40,40]], speed=0.5)
        )

    def Slalom(self):
        self.addCommands(
            SegmentFollowerCommand(
                [
                    [0, 13],
                    [-28, 16],
                    [-71, 26],
                    [-74, 64],
                    [-74, 198],
                    [-10, 206, True],
                    [28, 214, True],
                    [48, 235, True],
                    [48, 274, True],
                    [8, 286, True],
                    [-54, 260, True],
                    [-56, 228, True],
                    [32, 212],
                    [32, 30, True],
                    [-72, 34, True],
                    [-72, -36, True],
                ],
                maxSpeed=1.35,
                slowSpeed=0.9,
            ),
        )

    def BarellRacing(self):
        self.addCommands(
            SegmentFollowerCommand([[0, 116]], maxSpeed=1.3, stopWhenDone=True),
            SegmentFollowerCommand([[24, 0]], maxSpeed=1.3, stopWhenDone=False),
            DosadoCommand(36, startAngle=90, angleToTravel=280, maxSpeed=1, stopWhenDone=False, waitForAlign=True),
            SegmentFollowerCommand(
                [[0, 76]], maxSpeed=1.3, stopWhenDone=False, kP=0.04, 
            ),
            DosadoCommand(36, startAngle=180, angleToTravel=-270, reverseStrafe=True, stopWhenDone=False),
            SegmentFollowerCommand(
                [[36, 0], [74, 100], [74, 112]], maxSpeed=1.2, 
            ),
            DosadoCommand(
                44,
                startAngle=180,
                angleToTravel=180,
                reverseStrafe=True,
                waitForAlign=True
            ),
            SegmentFollowerCommand([[-14, -246]], maxSpeed=1.5),
        )

    def Bounce(self):
        self.addCommands(
            SegmentFollowerCommand([[0, 4]], maxSpeed=1, stopWhenDone=False),
            DosadoCommand(
                30,
                angleToTravel=95,
                startAngle=180,
                maxSpeed=1.2,
                waitForAlign=True,
                reverseStrafe=True,
                stopWhenDone=False,
            ),
            SegmentFollowerCommand([[-30, 0]], maxSpeed=1),
            InstantCommand(lambda: robot.drivetrain.stop(), [robot.drivetrain]),
            InstantCommand(lambda: robot.drivetrain.waitForRoll(), [robot.drivetrain]),
            SegmentFollowerCommand(
                [
                    [32, -2, {"speed": 0.6}],
                    [36, 14, {"speed": 1.1}],
                    [70, 20, {"speed": 1.1}],
                ],
                kP=0.0325,
                startPoint=[0, 0, {"speed": 0.6}],
                stopWhenDone=False,
            ),
            DosadoCommand(
                33,
                startAngle=90,
                angleToTravel=190,
                endAngle=-90,
                reverseForward=True,
                stopWhenDone=True,
                maxSpeed=1.25,
            ),
            SegmentFollowerCommand([[-76, -2]], maxSpeed=1.3, rearBonus=-0.15),
            InstantCommand(lambda: robot.drivetrain.stop(), [robot.drivetrain]),
            InstantCommand(lambda: robot.drivetrain.waitForRoll(), [robot.drivetrain]),
            SegmentFollowerCommand(
                [[78, -2]], maxSpeed=1.3, rearBonus=0.165, stopWhenDone=False
            ),
            DosadoCommand(
                52,
                startAngle=90,
                angleToTravel=190,
                endAngle=-90,
                reverseForward=True,
                stopWhenDone=True,
                maxSpeed=1.3,
            ),
            InstantCommand(lambda: robot.drivetrain.stop(), [robot.drivetrain]),
            SegmentFollowerCommand([[-78, 2]], maxSpeed=1.3, rearBonus=-0.15),
            InstantCommand(lambda: robot.drivetrain.stop(), [robot.drivetrain]),
            InstantCommand(lambda: robot.drivetrain.waitForRoll(), [robot.drivetrain]),
            SegmentFollowerCommand([[29, 3], [29, 40]], maxSpeed=1.3),
        )

    def GalacticSearchRedA(self):
        self.addCommands(
            InstantCommand(lambda: robot.intake.intakeBalls(0.9), [robot.intake]),
            WaitCommand(0.4),
            SegmentFollowerCommand(
                [
                    [0, 5, {"speed": 0.25}],
                    [0, 10, {"speed": 0.9}],
                    [30, 52, {"speed": 0.9}],
                    [-87, 56, {"speed": 1.1}],
                    [-87, 70, {"speed": 2.5}],
                    [-60, 300],
                ],
                maxSpeed=1.4,
            ),
        )

    def GalacticSearchRedB(self):
        self.addCommands(
            InstantCommand(lambda: robot.intake.intakeBalls(0.9), [robot.intake]),
            WaitCommand(0.4),
            SegmentFollowerCommand(
                [
                    [0, 5, {"speed": 0.25}], 
                    [0, 10, {"speed": 1}],
                    [50, 60, {"speed": 0.9}],
                    [-50, 130, {"speed":1.7}],
                    [-25, 430]
                ]
            ),
        )

    def interrupted(self):
        robot.intake.dontIntakeBalls()
        robot.chamber.stop()
        robot.conveyor.stop()
        robot.shooter.stopShooter()
