from .cougarsystem import *

import ports
import robot
import math

from networktables import NetworkTables


class Limelight(CougarSystem):
    """Subsystem for interacting with the limelight."""

    def __init__(self):
        super().__init__("limelight")

        self.nt = NetworkTables.getTable("limelight")

        self.driveTable = NetworkTables.getTable("DriveTrain")

        self.setPipeline(1)

    def setPipeline(self, pipeline: int):
        self.put("pipeline", pipeline)

    def getY(self):
        """
        Return the x-value to correct for the limelight being rotated.
        """
        return self.get("tx")

    def getX(self):
        """
        Return the y-value to correct for the limelight being rotated.
        """
        return self.get("ty")

    def getA(self):
        """
        Returns the area of the selected target.
        """
        return self.get("ta")

    def getTape(self):
        """
        Return whether or not tape is being detected by the limelight.
        """
        return self.get("tv") == 1

    def takeSnapShot(self):
        """
        Have the limelight take a snapshot.
        These can be viewed by connecting to the limelight
        with a USB cable.
        """
        self.put("snapshot", 1)
