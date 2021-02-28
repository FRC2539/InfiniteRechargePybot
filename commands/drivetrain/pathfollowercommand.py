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
    def get():
        thetaController = ProfiledPIDControllerRadians(
            0.001,
            0,
            0,
            TrapezoidProfileRadians.Constraints(
                constants.drivetrain.maxMetersPerSecond,
                constants.drivetrain.maxMetersPerSecondSquared,
            ),
        )  # Theta-controller
        thetaController.enableContinuousInput(-math.pi, math.pi)

        trajectory = GenerateTrajectoryCommand().getTrajectory(
            [
                [30, 30],
                [60, 60],
                [180, 60],
                [210, 30],
                [240, 0],
                [270, 30],
                [240, 60],
                [210, 30],
                [180, 0],
                [60, 0],
                [30, 30],
            ],
            [60, 0, 0],
        )

        command = Swerve4ControllerCommand(
            trajectory,
            robot.drivetrain.getSwervePose,
            robot.drivetrain.swerveKinematics,
            PIDController(0.005, 0, 0),  # X-controller
            PIDController(0.005, 0, 0),  # Y-controller
            thetaController,
            robot.drivetrain.setModuleStates,
            [robot.drivetrain],
        ).beforeStarting(
            lambda: robot.drivetrain.resetOdometry(
                trajectory.initialPose()
            )  # TODO: Find out if this breaks it.
        )

        return command
