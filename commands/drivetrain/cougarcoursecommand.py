from commands2 import CommandBase

from wpilib import Timer

import math
import robot

class CougarCourseCommand(CommandBase):
    
    def __init__(self, points: list, tolerance=1):
        """
        Distance is the distance we should travel in inches, turnOffset
        is the angle displacement of the gyro in degrees.
        """
        
        super().__init__()
        
        self.addRequirements([robot.drivetrain])
        
        additionalPoints = robot.drivetrain.injectPoints(points)
        self.allPoints = robot.drivetrain.smoothPoints(additionalPoints)
        self.allPoints = robot.drivetrain.assertDistanceAlongCurve(self.allPoints)
        
        self.tolerance = tolerance

        print('\n\n hi')
        
    def initialize(self):
        self.lastPosX = robot.drivetrain.getSwervePose().X() * 39.3701
        self.lastPosY = robot.drivetrain.getSwervePose().Y() * 39.3701
        
        self.inchesTravelledX = 0
        self.inchesTravelledY = 0
        
        self.lookAheadInches = 6
        
    def execute(self):
        self.inchesTravelledX = robot.drivetrain.getSwervePose().X() * 39.3701 - self.lastPosX + self.inchesTravelledX
        self.inchesTravelledY = robot.drivetrain.getSwervePose().Y() * 39.3701 - self.lastPosY + self.inchesTravelledY
        
        self.displacement = math.sqrt(self.inchesTravelledX**2 + self.inchesTravelledY**2)
        
        self.nextDistance = self.displacement + self.lookAheadInches
        
        for point in self.allPoints:
            self.targetX = point[0]
            self.targetY = point[1]
            if point[2] > self.nextDistance:
                break
            
        theta = math.degrees(math.atan((self.targetY - robot.drivetrain.getSwervePose().Y() * 39.3701) / (self.targetX - robot.drivetrain.getSwervePose().X() * 39.3701)))
        
        currentZ = math.sqrt(self.inchesTravelledX**2 + self.inchesTravelledY**2)
        
        toTravel = self.nextDistance - currentZ
        
        robot.drivetrain.setUniformModuleAngle(theta)
        robot.drivetrain.setUniformModulePercent(toTravel * 0.1)
            
    def isFinished(self):
        return ((abs(self.displacement) - abs(self.allPoints[-1][2])) <= self.tolerance )
        
    def end(self, interrupted):
        robot.drivetrain.stop()
