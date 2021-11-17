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

    def __init__(self, trajectory):
        super().__init__()

        self.addRequirements(robot.drivetrain)
        
        self.trajectory = trajectory
        
        self.driveController = HolonomicDriveController(
                PIDController(1, 0, 0),
                PIDController(1, 0, 0),
                ProfiledPIDControllerRadians(
                    1,
                    0,
                    0,
                    TrapezoidProfileRadians.Constraints(
                        constants.drivetrain.angularSpeedLimit,
                        constants.drivetrain.maxAngularAcceleration,
                    ),
                ),
        )
        
        self.timer = Timer()
        
        self.distanceTolerance = 0.4


    def initialize(self):
        self.timer.reset()
        
        self.timer.start()
        
        self.trajectoryDuration = self.trajectory.totalTime()
                
        self.finalState = self.trajectory.sample(self.trajectoryDuration).pose


    def execute(self):
        self.currentPose = robot.drivetrain.getSwervePose()
        
        self.currentTime = self.timer.get()
        
        trajectoryState = self.trajectory.sample(self.currentTime)
        
        #heading = trajectoryState.pose.rotation()
        heading = Rotation2d(0)
        
        chassisSpeeds = self.driveController.calculate(self.currentPose, trajectoryState, heading)
        
        robot.drivetrain.setChassisSpeeds(chassisSpeeds)
        
    def isFinished(self):
        timeUp = self.currentTime >= self.trajectoryDuration
        
        poseError = self.currentPose.relativeTo(self.finalState)
                
        atFinalLocation = abs(poseError.X()) < self.distanceTolerance and abs(poseError.Y()) < self.distanceTolerance
        
        print(timeUp, atFinalLocation, self.currentTime, self.trajectoryDuration)
        
        return atFinalLocation

    def end(self, interrupted):
        self.timer.stop()
