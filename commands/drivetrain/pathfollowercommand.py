from commands2 import InstantCommand, Swerve4ControllerCommand

from wpilib.controller import PIDController, ProfiledPIDControllerRadians

from wpimath.trajectory import TrapezoidProfileRadians

from .generatetrajectorycommand import GenerateTrajectoryCommand

import robot
import constants
import math


class PathFollowerCommand:
    def __init__(self):
        pass

    @staticmethod
    def get(translations, end):
        thetaController = ProfiledPIDControllerRadians(.00000000000000000000000000000000000001, 0, 0, TrapezoidProfileRadians.Constraints(math.pi, math.pi/100)) # Theta-controller NOTE: Error with this PID
        thetaController.enableContinuousInput(-math.pi, math.pi)
        
        t = GenerateTrajectoryCommand().getTrajectory(
                        translations, end) # [[x,y]], [x,y,theta]
        
        command = Swerve4ControllerCommand(
            t,
            robot.drivetrain.getSwervePose,
            robot.drivetrain.swerveKinematics,
            PIDController(.00000000000000000000000000000000000001, 0, 0), # X-controller
            PIDController(.00000000000000000000000000000000000001, 0, 0), # Y-controller
            thetaController,
            robot.drivetrain.setModuleStates,
            [robot.drivetrain]
        )
        
        # NOTE: Try this.
        command.resetOdometry(t.getInitialPose())
        
        return command.andThen(lambda: robot.drivetrain.stop(), [robot.drivetrain])

