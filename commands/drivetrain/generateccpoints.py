from commands2 import InstantCommand

import robot

class GenerateCCPoints(InstantCommand):
    
    def __init__(self, points):
        super().__init__()
        
        self.addRequirements([robot.drivetrain])
        
        self.allPoints = robot.drivetrain.injectPoints(points)
        self.allPoints = robot.drivetrain.smoothPoints(self.allPoints)
        self.allPoints = robot.drivetrain.assertDistanceAlongCurve(self.allPoints)
        
        # Reference all points. 
        