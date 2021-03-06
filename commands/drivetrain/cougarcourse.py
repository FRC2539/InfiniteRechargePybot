from commands2 import CommandBase

from wpilib import Timer

import robot

class CougarCourse(CommandBase):
    def __init__(self, points: list):
        """
        Distance is the distance we should travel in inches, turnOffset
        is the angle displacement of the gyro in degrees.
        """
        
        for x in points:
            if len(x) != 2:
                raise Exception('Points must have two values')
            
        
        
    def initialize(self):
        self.startPoseX = robot.drivetrain.getSwervePose().X()
        self.startPoseY = robot.drivetrain.getSwervePose().Y()
        
    def isFinished(self):
        return False