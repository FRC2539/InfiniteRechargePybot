from commands2 import CommandBase

import robot

from wpimath.trajectory import (
    TrajectoryGenerator,
    TrajectoryConfig,
    TrapezoidProfileRadians,
)

from wpimath.geometry import Translation2d, Rotation2d, Pose2d

from wpilib.controller import HolonomicDriveController
from wpilib.controller import PIDController, ProfiledPIDControllerRadians

import constants

from wpilib import Timer


class TrajectoryFollowerCommand(CommandBase):

    def __init__(self, trajectory, distanceTolerance=0.1):
        super().__init__()

        self.addRequirements(robot.drivetrain)
        
        self.trajectory = trajectory
        
        self.p = 1
        self.i = 0.2
        self.d = 0.03
        
        self.driveController = HolonomicDriveController(
                PIDController(self.p, self.i, self.d),
                PIDController(self.p, self.i, self.d),
                ProfiledPIDControllerRadians(
                    self.p,
                    self.i,
                    self.d,
                    TrapezoidProfileRadians.Constraints(
                        constants.drivetrain.angularSpeedLimit,
                        constants.drivetrain.maxAngularAcceleration,
                    ),
                ),
        )
        
        self.timer = Timer()
        
        self.distanceTolerance = distanceTolerance


    def initialize(self):
        self.timer.reset()
        
        self.timer.start()
        
        self.trajectoryDuration = self.trajectory.totalTime()
                
        self.finalState = self.trajectory.sample(self.trajectoryDuration).pose
        
        robot.drivetrain.addAutoPeriodicFunction(self.trajectoryFollowerExecute)

    def trajectoryFollowerExecute(self):
        robot.drivetrain.updateOdometry()
        
        self.currentPose = robot.drivetrain.getSwervePose()
        
        self.currentTime = self.timer.get()
        
        trajectoryState = self.trajectory.sample(
            self.currentTime + constants.drivetrain.autoPeriodicPeriod
        )
        
        #heading = trajectoryState.pose.rotation()
        heading = Rotation2d(0)
        
        chassisSpeeds = self.driveController.calculate(self.currentPose, trajectoryState, heading)
        
        robot.drivetrain.setChassisSpeeds(chassisSpeeds)
        
    def isFinished(self):
        self.currentTime = self.timer.get()
        
        timeUp = self.currentTime >= self.trajectoryDuration
        
        self.currentPose = robot.drivetrain.getSwervePose()
        
        distanceToTargetPosition = self.currentPose.translation().distance(
            self.finalState.translation()
        )
        
        atPosition = distanceToTargetPosition <= self.distanceTolerance
                
        return timeUp or atPosition

    def end(self, interrupted):
        self.timer.stop()
        
        robot.drivetrain.removeAutoPeriodicFunction(self.trajectoryFollowerExecute)
