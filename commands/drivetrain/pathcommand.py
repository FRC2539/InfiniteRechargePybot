from commands2 import CommandBase
import math

import robot


class PathCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.drivetrain)

    def initialize(self):
        self.lastPositions = robot.drivetrain.getPositions()
        self.lastSlope = [0, 0, 0, 0]
        self.totalDisplacements = [0, 0, 0, 0]
        self.speeds = [0.25, 0.25, 0.25, 0.25]
        # test path = x squared
        # test dy/dx = 2x

    def execute(self):

        currentPositions = robot.drivetrain.getPositions()
        displacements = []

        for lPosition, cPosition in zip(self.lastPositions, currentPositions):
            displacements.append(cPosition - lPosition)
            print(str(displacements[0]))
            
        for i, (d, m) in enumerate(zip(displacements, self.lastSlope)):
            print(str (m))
            self.totalDisplacements[i] += d * math.cos(math.tan(m))

        self.lastSlope = []
        angle = []
        self.lastPositions = currentPositions

        for dx in self.totalDisplacements:
            print('dx '+ str(dx))
            angle.append(math.atan(1/3600 * dx))
            self.lastSlope.append(1/3600 * dx)

        avg = sum(angle) / len(angle)
        robot.drivetrain.setUniformModuleAngle(avg)
        robot.drivetrain.setSpeeds(self.speeds)

        """
        displacements will be the distance along the x axis that has been traveled
        always starting at 0,0
        """

    def end(self, interrupted):
        robot.drivetrain.stop()
