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
            0.00001, 0, 0, TrapezoidProfileRadians.Constraints(2 * math.pi, math.pi)
        )  # Theta-controller NOTE: Error with this PID
        thetaController.enableContinuousInput(-math.pi, math.pi)

        # Do you have a JSON or points?
        if type(translations) is str:
            trajectory = GenerateTrajectoryCommand().getTrajectory(
                translations, end
            )  # TrajectoryUtil.fromPathweaverJson(translations)
        else:
            trajectory = GenerateTrajectoryCommand().getTrajectory(
                translations, end
            )  # [[x,y]], [x,y,theta],

        command = Swerve4ControllerCommand(
            trajectory,
            robot.drivetrain.getSwervePose,
            robot.drivetrain.swerveKinematics,
            PIDController(0.01, 0, 0),  # X-controller
            PIDController(0.01, 0, 0),  # Y-controller
            thetaController,
            robot.drivetrain.setModuleStates,
            [robot.drivetrain],
        )

        return command.andThen(lambda: robot.drivetrain.stop(), [robot.drivetrain])
