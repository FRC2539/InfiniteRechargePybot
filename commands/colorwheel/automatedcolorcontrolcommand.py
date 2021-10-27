from commands2 import CommandBase

import robot

from networktables import NetworkTables


class AutomatedColorControlCommand(CommandBase):
    def __init__(self, targetColor=None):
        super().__init__()

        self.addRequirements(robot.chamber, robot.colorwheel)

        # Algorithm overview
        # Determine the current color being detected
        # Move the wheel until you are on the color "2 colors"
        #   away from the correct one (to account for being 90 degrees off)

        self.colors = robot.colorwheel.getColorsList()

        self.colorOrder = [
            "R",
            "Y",
            "B",
            "G",
        ]

        self.fmsInfoTable = NetworkTables.getTable("FMSInfo")

    def initialize(self):
        # Find which color we are positioned on, on the color wheel
        self.updateColorReadings()

        colorFromNetworkTables = self.fmsInfoTable.getValue("GameSpecificMessage")

        # Find the index of goal color in the colors list
        colorIndex = self.colorOrder.index(colorFromNetworkTables)

        # Store the color we are getting from network tables
        self.goalColor = self.colors[colorIndex]

        # Find which color we need to move the wheel to
        # (accounts for the 90 degree offset)
        targetIndex = (colorIndex + 2) % len(self.colors)

        self.targetColor = self.colors[targetIndex]

    def updateColorReadings(self):
        self.currentColor = robot.colorwheel.getColor()

    def execute(self):
        robot.chamber.spinColorWheelSlow()

    def isFinished(self):
        self.updateColorReadings()

        if self.currentColor == self.targetColor:
            return True
        else:
            return False

    def end(self, interrupted):
        robot.chamber.stop()
