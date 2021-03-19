from commands2 import InstantCommand

from wpimath.trajectory import TrajectoryGenerator, TrajectoryConfig, Trajectory

from wpimath.geometry import Pose2d, Translation2d, Rotation2d

import robot
import constants
import math


class GenerateTrajectoryCommand:
    
    @staticmethod
    def getTrajectory(movements_: list, endPose: list, startingPose: list = [0, 0, 0]):
        config = TrajectoryConfig(
            constants.drivetrain.maxMetersPerSecond,  # Max meters per second
            constants.drivetrain.maxMetersPerSecondSquared,  # Max meters per second squared
        )

        config.setKinematics(
            robot.drivetrain.swerveKinematics
        )

        initialPosition = Pose2d(
            startingPose[0],
            startingPose[1],
            Rotation2d(startingPose[2]),
        )

        movements = []
        for point in movements_:
            try:
                movements.append(
                    Translation2d(point[0], point[1])
                )
            except (TypeError):
                raise Exception("Type Error Occurred.")

        endPosition = Pose2d(
            endPose[0], endPose[1], Rotation2d(endPose[2])
        )

        trajectory = TrajectoryGenerator.generateTrajectory(
            initialPosition,
            movements,
            endPosition,
            config,
        )

        return trajectory
