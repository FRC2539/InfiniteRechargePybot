from commands2 import InstantCommand, Swerve4ControllerCommand

from wpilib.controller import PIDController, ProfiledPIDControllerRadians

from wpimath.trajectory import TrapezoidProfileRadians, TrajectoryUtil

from .generatetrajectorycommand import GenerateTrajectoryCommand

import robot
import constants
import math


class PathFollowerCommand:
    def __init__(self):
        pass

    @staticmethod
    def get(translations, end=None):
        thetaController = ProfiledPIDControllerRadians(
            0.0000001, 0, 0.1, TrapezoidProfileRadians.Constraints(.5*math.pi, .25*math.pi)
        )  # Theta-controller NOTE: Error with this PID
        thetaController.enableContinuousInput(-math.pi, math.pi)

        # Do you have a JSON or points?
        if type(translations) is str:
            trajectory = TrajectoryUtil.fromPathweaverJson(translations)
        else:
            trajectory = GenerateTrajectoryCommand().getTrajectory(
                translations, end
            )  # [[x,y]], [x,y,theta],

        command = Swerve4ControllerCommand(
            trajectory,
            robot.drivetrain.getSwervePose,
            robot.drivetrain.swerveKinematics,
            PIDController(0.000000001, 0, 0.2),  # X-controller
            PIDController(0.000000001, 0, 0.2),  # Y-controller
            thetaController,
            robot.drivetrain.setModuleStates,
            [robot.drivetrain],
        )

        return command.andThen(lambda: robot.drivetrain.stop(), [robot.drivetrain])
