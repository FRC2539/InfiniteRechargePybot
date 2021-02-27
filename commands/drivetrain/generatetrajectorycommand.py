from commands2 import InstantCommand

from wpimath.trajectory import TrajectoryGenerator, TrajectoryConfig, Trajectory

from wpimath.geometry import Pose2d, Translation2d, Rotation2d

import robot


class GenerateTrajectoryCommand(InstantCommand):

    def __init__(self, movements_: list, endPose: list, startingPose: list = [0, 0, 0]):
        super().__init__()
        
        self.addRequirements(robot.drivetrain)

        config = TrajectoryConfig(
            1, # Max meters per second
            0.1, # Max meters per second squared
        )
        #config.setKinematics(robot.drivetrain.swerveKinematics) BUG: Type not clarified for acceptance.
                
        initialPosition = Pose2d(
            startingPose[0]/-4*2.54/100,
            startingPose[1]/-4*2.54/100,
            Rotation2d(startingPose[2])
        )
        
        print(movements_)
        
        movements = []
        for point in movements_:
            try:
                movements.append(Translation2d(point[0]/-4*2.54/100, point[1]/-4*2.54/100))
            except(TypeError):
                raise Exception('Give lists in the movements_ list consisting of your x and y coordinates. You gave: ' + str(movements_))

        finalPosition = Pose2d(
            endPose[0]/-4*2.54/100,
            endPose[1]/-4*2.54/100,
            Rotation2d(endPose[2])
        )
        
        self.trajectory = TrajectoryGenerator.generateTrajectory(
            initialPosition, 
            movements,
            finalPosition,
            config,
        )

    def getTrajectory(self):
        robot.drivetrain.resetOdometry(self.trajectory.initialPose())
        
        return self.trajectory
