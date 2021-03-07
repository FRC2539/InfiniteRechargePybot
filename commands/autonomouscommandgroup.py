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
from commands.drivetrain.pathfollowercommand import PathFollowerCommand
from commands.drivetrain.cougarcoursecommand import CougarCourseCommand

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
        
        self.Slalom()
    
       # eval("self." + toRun + "()")  # Setups the method.

    def example(self):
        self.addCommands(InstantCommand(lambda: print("I worked!")))

    def tenBall(self):
        self.addCommands(InstantCommand(lambda: print("Number two worked!")))

        # self.conveyor = InstantCommand(robot.conveyor.forward, [robot.conveyor])

        # self.turnBack = TurnCommand(20)
        # self.realign = TurnCommand(-10)

        # self.intake = InstantCommand(robot.intake.intakeBalls, [robot.intake])
        # self.moveSide = MoveCommand(7.071, angle=45, slow=True)

        # self.moveForward = MoveCommand(199, slow=True)

        # self.stopIntake = InstantCommand(robot.intake.dontIntakeBalls, [robot.intake])
        # self.moveBack = MoveCommand(-120, angle=14)

        # self.sudo = AutomatedShootCommand(3000).withTimeout(4)
        # self.sudoNT = AutomatedShootCommand()

        # self.goBack = self.moveBack.alongWith(self.sudoNT)

        # self.addCommands(
        #                  #self.conveyor,
        #                  self.sudo,
        #                  self.turnBack,
        #                  self.intake,
        #                  self.moveSide,
        #                  self.moveForward,
        #                  self.realign,
        #                  self.goBack,
        #                  )

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

        self.print = InstantCommand(lambda: print("\n\nEnd\n\n"))

        self.moveForward = MoveCommand(124)
        self.secondMove = MoveCommand(112, angle=2)
        self.moveBack = MoveCommand(-24, angle=-1.5)
        self.turnToTarget = TurnCommand(-20)

        self.shoot = AutomatedShootCommand(3800).withTimeout(3.25)
        self.shootTwo = AutomatedShootCommand(3800)

        rotate = math.pi

        # Schedule the autonomous command
        self.auton = PathFollowerCommand().get(
            [[3.586, -4.228], [4.519, -3.042], [3.485, -2.159], [2.375, -3.224]],[3.6, -4.228, 0]
             #'/home/lvuser/py/Slalmon.wpilib.json'
            # working 10 ball
            #[[-120, -12], [-177, -67]],
            #[-124, -70, math.pi],
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
            self.print
            # self.moveBack,
            # self.turnToTarget,
            # self.shootTwo        # 4 seconds
        )
        
    def Slalom(self):
                
        self.addCommands(
            CougarCourseCommand()
            )
            
    def interrupted(self):
        robot.intake.dontIntakeBalls()
        robot.chamber.stop()
        robot.conveyor.stop()
        robot.shooter.stopShooter()
