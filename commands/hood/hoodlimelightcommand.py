from commands2 import CommandBase

import robot

class HoodLimelightCommand(CommandBase):
    """Adjusts the position of the hood with input from the limelight."""
    def __init__(self):
        super().__init__()
        
        self.addRequirements(robot.hood)
        
        self.yOffsetP = 35 # A proportion to scale the error to a speed the motor can use.
        
    def initialize(self):
        robot.limelight.setPipeline(0)
    
    def execute(self):
        yOffset = -robot.limelight.getY() # Returns an angle
        
        yPercentError = yOffset / self.yOffsetP # This value is found experimentally
        
        robot.hood.move(yPercentError)
    
    def end(self, iterrupted):
        robot.hood.stop()
