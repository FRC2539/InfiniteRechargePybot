from commands2 import CommandBase

import math

import robot, constants

# Used in the align() method.
loopCount = 0


def align(angle):
    global loopCount

    loopCount += 1

    count = 0
    if angle < 0:
        angle += 360
    for a in robot.drivetrain.getModuleAngles():
        if abs(a - angle) < 3 or (
            a > 357 and abs(angle) < 2
        ):  # The 'or' is a temporary fix.
            count += 1

    if count >= 3:  # TODO: Tune the max loop count.
        return True

    return False


class CougarCourseCommand(CommandBase):
    """
    Different than the old Cougar Course. Works
    like a Bezier command however the trajectory
    should pass through the defined points. This
    makes them much eaiser to interpret and write
    on the fly.
    """

    def __init__(self, points: list, speed=1, graphAtSim=False, name=""):
        super().__init__()

        self.addRequirements(robot.drivetrain)

        self.points = points  # The desired points to drive through.
        self.speed = speed  # The percent of maxSpeed at which this should be run.

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

        self.curveLength = robot.drivetrain.estimateLengthCougarCourse(
            self.cX, self.cY
        )  # The estimated length of the curve.

        self.t = 0  # Percentage of the curve which we have completed

    def initialize(self):
        # The position of the back left module.
        self.startPos = robot.drivetrain.getPositions()[2]

        # The angle component.
        self.angle = self.angleFunc(self.t)

        if self.angle > 180:
            self.angle -= 360

        # Set the initial angle of the wheels.
        robot.drivetrain.setUniformModuleAngle(self.angle)

        while not align(self.angle):
            pass

        # Set the speed of the drivetrain.
        robot.drivetrain.setUniformModuleSpeed(self.speed)

    def execute(self):
        # Update the completion percentage as we move.
        self.t = abs(
            (robot.drivetrain.getPositions()[2] - self.startPos) / self.curveLength
        )

        # Are we done?
        if self.t >= 1:
            robot.drivetrain.stop()

        # Calculate the angle of the wheels.
        self.angle = self.angleFunc(self.t)

        if self.angle > 180:
            self.angle -= 360

        # Set the angle of the wheels.
        robot.drivetrain.setUniformModuleAngle(self.angle)
        
        print(self.t)

    def isFinished(self):
        # We are done when we have travelled 100% of the curve.
        return self.t >= 1

    def end(self, interrupted):
        robot.drivetrain.stop()
