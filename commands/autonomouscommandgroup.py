from wpilib import DriverStation

from commands2 import (
    SequentialCommandGroup,
    ParallelCommandGroup,
    CommandBase,
    InstantCommand,
    Swerve4ControllerCommand,
)

from commands.drivetrain.turncommand import TurnCommand
from commands.drivetrain.movecommand import MoveCommand
from commands.drivetrain.generatevectors import GenerateVectors
from commands.drivetrain.pathfollowercommand import PathFollowerCommand
from commands.drivetrain.cougarcoursecommand import CougarCourseCommand
from commands.drivetrain.runautocommand import RunAutoCommand
from commands.drivetrain.segmentfollowercommand import SegmentFollowerCommand

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

        self.BarellRacing()

    # eval("self." + toRun + "()")  # Setups the method.

    def example(self):
        self.addCommands(InstantCommand(lambda: print("I worked!")))

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

    # def Slalom(self):
    #     self.addCommands(CougarCourseCommand(1))

    def BarellRacing(self):
        self.addCommands(
            # SegmentFollowerCommand([[30, 30], [60, 0]]), # PathFollowerCommand.get([[-2,-2]], [0,-4,0])
            SegmentFollowerCommand(
                [
                    [0, 105],
                    [15, 120],
                    [30, 135],
                    [45, 120],
                    [60, 105],
                    [45, 90],
                    [30, 75],
                    [15, 90],
                    [0, 105],
                    [0, 180],
                    [-30, 210],
                    [-60, 180],
                    [-30, 150],
                    [0, 180],
                    [60, 210],
                    [60, 240],
                    [30, 270],
                    [0, 240],
                    [0, 0],
                ]
            )
        )

    # def Bounce(self):
    #     self.addCommands(CougarCourseCommand(3))

    def interrupted(self):
        robot.intake.dontIntakeBalls()
        robot.chamber.stop()
        robot.conveyor.stop()
        robot.shooter.stopShooter()
