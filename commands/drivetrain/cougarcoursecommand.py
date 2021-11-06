from commands2 import CommandBase

import robot


class CougarCourseCommand(CommandBase):
    """
    Different than the old Cougar Course. Works
    like a Bezier command however the trajectory 
    should pass through the defined points. This
    makes them much eaiser to interpret and write
    on the fly.
    """

    def __init__(self, points: list):
        super().__init__()

        self.addRequirements(robot.drivetrain)
        self.points = points

    def initialize(self):
        robot.drivetrain.parametricSplineGenerator(self.points)

    def execute(self):
        pass


    def end(self, interrupted):
        pass
