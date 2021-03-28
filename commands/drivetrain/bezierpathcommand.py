from commands2 import CommandBase

import robot


class BezierPathCommand(CommandBase):

    def __init__(self, maxSpeed=1):
        """
        This command will make the robot follow a quadratic or cubic Bezier
        curve. NOTE: Give the code four points for a cubic, or three for a 
        quadratic!
        """
        
        super().__init__()

        self.addRequirements(robot.drivetrain)


    def initialize(self):
        pass


    def execute(self):
        pass

    def end(self, interrupted):
        pass
