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
from commands.drivetrain.pathfollowercommand import PathFollowerCommand

from commands.intake.intakecommand import IntakeCommand

from commands.limelight.automatedshootcommand import AutomatedShootCommand

from wpilib.controller import PIDController, ProfiledPIDControllerRadians

import math
import robot


class AutonomousCommandGroup(SequentialCommandGroup):
    def __init__(self):
        super().__init__()

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
        
        self.conveyor = InstantCommand(robot.conveyor.forward, [robot.conveyor])

        self.turnBack = TurnCommand(20)
        self.realign = TurnCommand(-10)

        self.intake = InstantCommand(robot.intake.intakeBalls, [robot.intake])
        self.moveSide = MoveCommand(7.071, angle=45, slow=True)

        self.stopIntake = InstantCommand(robot.intake.dontIntakeBalls, [robot.intake])
        self.moveBack = MoveCommand(-120, angle=14)

        self.sudo = AutomatedShootCommand(3500).withTimeout(4)
        self.sudoNT = AutomatedShootCommand()

        self.goBack = self.moveBack.alongWith(self.sudoNT)
        

        self.spinUp = InstantCommand(lambda: robot.shooter.setRPM(3500), [robot.shooter])
        self.grabBalls = InstantCommand(lambda: robot.intake.intakeBalls(), [robot.intake])
        self.stopGrabbing = InstantCommand(lambda: robot.intake.dontIntakeBalls, [robot.intake])
        self.conveyorRun = InstantCommand(lambda: robot.conveyor.forward(), [robot.conveyor])
                
        self.moveForward = MoveCommand(124, slow=True)
        self.shoot = AutomatedShootCommand(3500).withTimeout(5)


        rotate = math.pi

        # Schedule the autonomous command
        self.auton = PathFollowerCommand().get(#[[36, 0, rotate], [72, 0, rotate / 2]])
                [[112, 0], [0, 0], [-124, -58]], [-68, -88, 0]
            ) # driverhud.getAutonomousProgram()
        
        self.addCommands(
                        self.spinUp,      # ~
                        self.grabBalls,   # ~ All total to
                        self.conveyorRun, # ~ 3 seconds ideally
                        self.moveForward, # ~ 
                        self.shoot,       # - These two should total
                        self.spinUp,      # - about 3 seconds, assuming up to speed.
                        self.auton,       # 5 seconds
                        self.shoot        # 4 seconds
                        ) 

    def interrupted(self):
        robot.intake.dontIntakeBalls()
        robot.chamber.stop()
        robot.conveyor.stop()
        robot.shooter.stopShooter()
