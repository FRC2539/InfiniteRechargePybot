from commands2 import InstantCommand

from wpimath.trajectory import TrajectoryGenerator, TrajectoryConfig, Trajectory

from wpimath.geometry import Pose2d, Translation2d, Rotation2d

import robot


class GenerateTrajectoryCommand(InstantCommand):

    def __init__(self, movements_: list, endPose: list, startingPose: list = [0, 0, 0]):
        super().__init__()

        self.addRequirements(robot.drivetrain)

        config = TrajectoryConfig(
            4, # Max meters per second
            2 # Max meters per second squared
        )
                
        initialPosition = Pose2d(
            startingPose[0],
            startingPose[1],
            Rotation2d(startingPose[2])
        )
        
        movements = []
        for point in movements_:
            try:
                movements.append(Translation2d(point[0], point[1]))
            except(TypeError):
                raise Exception('Give lists in the movements_ list consisting of your x and y coordinates. You gave: ' + str(movements_))

        finalPosition = Pose2d(
            endPose[0],
            endPose[1],
            Rotation2d(endPose[2])
        )
        
        self.trajectory = TrajectoryGenerator.generateTrajectory(
            initialPosition, 
            movements,
            finalPosition,
            config,
        )

    def getTrajectory(self):
        return self.trajectory
