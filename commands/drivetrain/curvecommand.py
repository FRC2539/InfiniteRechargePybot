from wpilib.command import Command

import math

import robot


class CurveCommand(Command):

    def __init__(self, x, y):
        
        '''
        My strategy going into this is to going to be distances and heading:
        Start with a set (x, y) goal, assuming we start at zero. Calculate the chord length, arc length, 
        central angle, and the radius. With that, we can also create the equation of the circle 
        we will be traveling. We now have what we need to start moving. First, find the current 
        central angle by using ratio between the arc length and our position on the arc. Take this and
        the radius and find the cord length. Now find the two other angles in the isoceles triangle
        with the radius and central angle. Subtract 90 by the newly found angle, do some right triangle
        trigonometry and calculate the x and y of your current position. Take the slope of where you are
        (put x in the derivative of circle equation we made earlier), and then convert that slope to degrees with 
        trigonometry. Finally, set your wheel angles to this angle, and keep a constant speed. Stop the wheels 
        when they ALL have traveled the distance of the arc length. Ouch. LOL just realized this doesn't ever
        need the NavX, just the wheel angles. Remarkable. 
        
        -Ben
        '''
        
        super().__init__('Curve')
        
        self.x = x # End x-coordinate
        self.y = y # End y-coordinate
        self.z = math.sqrt((self.x**2) + (self.y)**2) # The hypotenuse between start and goal, the chord. 
        
        self.a = math.degrees(math.atan(self.x / self.y)) # The angle between the hypotenuse and the y-side (degrees). 
        self.theta = 90 - self.a # 90 - angle in triangle. 
        
        self.b = 180 - (2 * self.theta) # self.b is the central angle
        self.radius = (self.z / 2) / math.cos(self.theta * (math.pi / 180))
        # Radius of the circle we will be traveling. Create right triangle with half of the chord.
        
        self.totalArcLength = (self.b * (math.pi / 180)) * self.radius # The total length of our path.

        self.requires(robot.drivetrain)

    def initialize(self):
        pass


    def execute(self):
        self.currentAL = 0 # Update this with the encoders. Current arc length.
        self.desiredHeading = self.calcPosition()
        
    def isFinished(self):
        pass

    def end(self):
        pass
    
    def calcPosition(self):
        self.currentCA = (self.currentAL / self.totalArcLength) * self.b # Current central angle in degrees of where we are along path. 
        self.currentCL = 2 * self.radius * math.sin((self.currentCA / 2) * (math.pi / 180)) # Current chord length. 'a' on my paper.
        
        self.angleZ = (180 - self.currentCA) / 2 # The angle in the isoceles triangle, in degrees.
        self.q = 90 - self.angleZ # The angle, in degrees, next to one of the angle z's.
        
        self.currentX = math.sin(self.q * (math.pi / 180)) * self.currentCL
        # Use the self.q angle, which is next to an angle z, and the current chord length to find the opposite, x, length. 
        
        return 90 - self.getSlopeToSet(self.currentX) 
        # Finds the slope at the current x with easy calculus and returns that in degrees above the horizontal (so subtract it from 90 ;) ).

    def getSlopeToSet(self, x): 
        return (math.atan((-x / (math.sqrt(self.radius**2 - x**2))))) * 180 / math.pi
        # Return the slope in degrees using first derivative. 