from commands2 import InstantCommand

from wpimath.trajectory import TrajectoryGenerator, TrajectoryConfig, Trajectory

from wpimath.geometry import Pose2d, Translation2d, Rotation2d

import robot
import constants


class GenerateTrajectoryCommand:
    @staticmethod
    def getTrajectory(movements_: list, endPose: list, startingPose: list = [0, 0, 0]):
        config = TrajectoryConfig(
            constants.drivetrain.maxMetersPerSecond,  # Max meters per second
            constants.drivetrain.maxMetersPerSecondSquared,  # Max meters per second squared
        )
        config.setKinematics(robot.drivetrain.swerveKinematics) # BUG: Type not clarified for acceptance.

        initialPosition = Pose2d(
            startingPose[0] / -4 * 2.54 / 100,
            startingPose[1] / -4 * 2.54 / 100,
            Rotation2d(startingPose[2]),
        )

        movements = []
        for point in movements_:
            try:
                movements.append(
                    Translation2d(
                        point[0] / -4 * 2.54 / 100, point[1] / -4 * 2.54 / 100
                    )
                )
            except(TypeError, IndexError) as e:
                if e == TypeError:
                    raise Exception(
                        "Give lists in the movements_ list consisting of your x and y coordinates. You gave: "
                        + str(movements_)
                    )
                elif e == IndexError:
                    raise Exception(
                        "Uh oh! You got an index error; does each sublist have two numerical values that are separated by a comma? Movements: "
                        + str(movements_)
                    )

        finalPosition = Pose2d(
            endPose[0] / -4 * 2.54 / 100,
            endPose[1] / -4 * 2.54 / 100,
            Rotation2d(endPose[2]),
        )

        trajectory = TrajectoryGenerator.generateTrajectory(
            initialPosition,
            movements,
            finalPosition,
            config,
        )

        return trajectory
