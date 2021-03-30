from commands2 import CommandBase

import math

import robot

# Counts how many iterations we've done in align().
loopCount = 0

def align(angle):
    global loopCount

    loopCount += 1
    
    count = 0
    if angle < 0:
        angle += 360
    for a in robot.drivetrain.getModuleAngles():
        if abs(a - angle) < 5:
            count += 1

    if count >= 3 or loopCount > 50: # TODO: Tune the max loop count.
        return

    align(angle)


class BezierPathCommand(CommandBase):

    def __init__(self, points: list, speed=1):
        """
        This command will make the robot follow a quadratic or cubic Bezier
        curve. NOTE: Give the code four points for a cubic, or three for a 
        quadratic! Give the points in inches please!
        """
        
        super().__init__()

        self.addRequirements(robot.drivetrain)

        # Use a quadratic Bezier.
        if len(points) == 3:
            self.getSlope = robot.drivetrain.getQuadraticBezierSlope
            self.getLength = robot.drivetrain.getQuadraticBezierLength
            self.getPosition = robot.drivetrain.getQuadraticBezierPosition
        
        # Use a cubic Bezier.
        elif len(points) == 4:
            self.getSlope = robot.drivetrain.getCubicBezierSlope
            self.getLength = robot.drivetrain.getCubicBezierLength
            self.getPosition = robot.drivetrain.getCubicBezierPosition
        
        # You didn't give three or four points.
        else:
            raise Exception(f'Please provide four points for a cubic Bezier curve, or three points for a quadratic Bezier curve. You gave ${len(points)} points!')
    
        self.points = points
        self.speed = speed
        
        self.t = 0
        
        self.curveLength = self.getLength(self.points)
        
    def initialize(self):
        # Reset out variables.
        self.t = 0
        loopCount = 0
        
        # Get the start position of the back left module.
        self.startPos = robot.drivetrain.getPositions()[2]
    
        slopeComponents = self.getSlope(self.points, self.t)
        angle = math.atan2(slopeComponents[0], slopeComponents[1]) * 180 / math.pi + 90
        
        if angle > 180:
            angle -= 360
            
        # Set and wait for the module angles to go to the right position.
        robot.drivetrain.setUniformModuleAngle(angle)
        align(angle)
    
        # Set the drive speed.
        robot.drivetrain.setUniformModuleSpeed(self.speed)
    
    def execute(self):
        # 'self.t' is the percent of the curve which we have traversed. We use it to calculate our heading.
        self.t = abs((robot.drivetrain.getPositions()[2] - self.startPos) / self.curveLength)
    
        # Calculate and set the angle.
        slopeComponents = self.getSlope(self.points, self.t)
        angle = math.atan2(slopeComponents[0], slopeComponents[1]) * 180 / math.pi + 90
        
        if angle > 180:
            angle -= 360
        
        if self.t != 1:    
            robot.drivetrain.setUniformModuleAngle(angle)
                
    def isFinished(self):
        # We are done when we have travelled 100% of the curve.
        return self.t >= 1
    
    def end(self, interrupted):
        # Stop moving when we're done.
        robot.drivetrain.stop()
