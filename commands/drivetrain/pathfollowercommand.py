from commands2 import InstantCommand, Swerve4ControllerCommand

from wpilib.controller import PIDController, ProfiledPIDControllerRadians

from wpimath.trajectory import TrapezoidProfileRadians

from .generatetrajectorycommand import GenerateTrajectoryCommand

import robot
import math


class PathFollowerCommand:

    def __init__(self):
        pass

    @staticmethod
    def get():                 
        thetaController = ProfiledPIDControllerRadians(0.1, 0, 0, TrapezoidProfileRadians.Constraints(4, 2)) # Theta-controller
        thetaController.enableContinuousInput(-math.pi, math.pi)
               
        command = Swerve4ControllerCommand(
            GenerateTrajectoryCommand(
                    [[1, 1], [2, -1]], [3, 0, 0]
                    ).getTrajectory(),
            robot.drivetrain.getSwervePose,
            robot.drivetrain.swerveKinematics,
            PIDController(0.1, 0, 0), # X-controller
            PIDController(0.1, 0, 0), # Y-controller
            thetaController,
            robot.drivetrain.setModuleStates,
            [robot.drivetrain]
        )
        
        return command
