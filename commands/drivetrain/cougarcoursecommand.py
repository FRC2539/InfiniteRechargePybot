from commands2 import CommandBase

import math

import robot, constants


class CougarCourseCommand(CommandBase):
    """
    Different than the old Cougar Course. Works
    like a Bezier command however the trajectory
    should pass through the defined points. This
    makes them much eaiser to interpret and write
    on the fly.
    """

    def __init__(self, points: list, graphAtSim=False, name=""):
        super().__init__()

        self.addRequirements(robot.drivetrain)
        
        self.points = points    # The desired points to drive through.

        self.cX, self.cY = robot.drivetrain.calculateCoefficientsCougarCourse(
            self.points
        )

        self.posFunc = robot.drivetrain.setCoefficientsPosCougarCourse(self.cX, self.cY)
        self.angleFunc = robot.drivetrain.setCoefficientsSlopeCougarCourse(
            self.cX, self.cY
        )
        
        if graphAtSim:
            
            try:
                lastNum = list(constants.drivetrain.coursesToGraph.keys())[-1]
            except IndexError:
                lastNum = -1
                
            if name == "":
                name = "Course #" + str(lastNum + 1)
                
            constants.drivetrain.coursesToGraph[lastNum + 1] = (self.posFunc, name)

        self.curveLength = robot.drivetrain.estimateLengthCougarCourse(self.cX, self.cY)    # The estimated length of the curve.

        self.t = 0              # Percentage of the curve which we have completed
        
    def initialize(self):
        pass

    def execute(self):
        pass

    def end(self, interrupted):
        pass
