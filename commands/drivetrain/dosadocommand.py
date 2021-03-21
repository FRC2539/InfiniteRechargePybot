from commands2 import CommandBase

from robotpy_ext.misc import NotifierDelay

import robot, constants
    
import math

class DosadoCommand(CommandBase):
    def __init__(self, radius, startAngle=90, angleToTravel=180, velocity=0.8):
        """
        Note that startAngle is the module angles. The default is 90,
        which would be to the right of the robot's orientation. The angle
        to travel is how many degrees it should travel in total. Velocity is
        a percent of the max speed.
        """
        super().__init__()
        
        self.addRequirements([robot.drivetrain])
        
        self.velPercent = velocity
        self.linearVelocity = velocity * constants.drivetrain.speedLimit
        self.radius = radius
        self.angle = startAngle
        self.angleToTravel = angleToTravel
        
        if self.angle < 0:
            self.idToIndex = 0
        else:
            self.idToIndex = 1
            
        self.totalArcLength = (self.angleToTravel * math.pi / 180) * self.radius
        self.revPerSecond = (self.linearVelocity / self.radius)
            
    def initialize(self):
        robot.drivetrain.setModuleProfiles(1, drive=False) # Use the secondary PIDs for the turn motor.
        self.startPos = robot.drivetrain.getPositions()[self.idToIndex]
        self.done = False
        
    def execute(self):
        currentDistAlongArc = abs(robot.drivetrain.getPositions()[self.idToIndex] - self.startPos)
        print('cda ' + str(currentDistAlongArc))
        if currentDistAlongArc >= abs(self.totalArcLength):
            self.done = True
        else:
            theta = currentDistAlongArc / self.radius # The remaining angle.
            forward = -self.revPerSecond * self.radius * math.cos(theta) / abs(self.linearVelocity)
            strafe = self.revPerSecond * self.radius * math.sin(theta) / abs(self.linearVelocity)
            
            print('f ' + str(forward))
            
            speeds, angles = robot.drivetrain._calculateSpeeds(strafe, forward, 0)
            
            speeds = [s * abs(self.velPercent) for s in speeds] 
            angles = [a - self.angle for a in angles]
            
            print('a ' + str(angles))
            print('actual angle ' + str(robot.drivetrain.getModuleAngles()))
            
            robot.drivetrain.setSpeeds(speeds)
            robot.drivetrain.setModuleAngles(angles)
            
    def isFinished(self):
        return self.done
    
    def end(self, interrupted):
        robot.drivetrain.setModuleProfiles(0, drive=False)