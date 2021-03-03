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

        #config.setKinematics(robot.drivetrain.swerveKinematics) BUG: Type not clarified for acceptance.
        
        conversion = -4.2134465 * 100 / 2.54
        #rotconv = 1 #-1
        #initialPosition = Pose2d(
            
            #startingPose[0]/conversion,
            #startingPose[1]/conversion,
            #Rotation2d(startingPose[2]/rotconv)
        #)
        
        
        initialPosition = Pose2d(
            startingPose[0]/conversion,
            startingPose[1]/conversion,
            Rotation2d(startingPose[2])
        )
            
        movements = []
        for point in movements_:
            try:
                movements.append(Translation2d(point[0]/conversion, point[1]/conversion))
            except(TypeError):
                raise Exception('Type Error Occurred.')
           
        endPosition = Pose2d(
            endPose[0]/conversion,
            endPose[1]/conversion,
            Rotation2d(endPose[2])
        )
           
        trajectory = TrajectoryGenerator.generateTrajectory(
            initialPosition,
            movements,
            endPosition,
            config,
        )

        #movements = []
        #for point in movements_:
            #try:
                #movements.append(Pose2d(point[0]/conversion, point[1]/conversion, Rotation2d(point[2]/rotconv)))
            #except(TypeError):
                #raise Exception('Give lists in the movements_ list consisting of your x and y coordinates. You gave: ' + str(movements_))

        #movements.insert(0, initialPosition)

        #print('\n\n\n\n ' + str(movements))

        #trajectory = TrajectoryGenerator.generateTrajectory(
            #movements,
            #config,
        #)
        
        robot.drivetrain.resetOdometry(trajectory.initialPose())

        return trajectory
