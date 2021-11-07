from commands2 import CommandBase

import math

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

        self.cX, self.cY = robot.drivetrain.calculateCoefficientsCougarCourse(
            self.points
        )

        self.posFunc = robot.drivetrain.setCoefficientsPosCougarCourse(self.cX, self.cY)
        self.angleFunc = robot.drivetrain.setCoefficientsSlopeCougarCourse(
            self.cX, self.cY
        )

    def initialize(self):
        pass

    def execute(self):
        pass

    def end(self, interrupted):
        pass
