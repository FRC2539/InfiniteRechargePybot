from .cougarsystem import *

import ports
import robot
import constants
import math

from networktables import NetworkTables


class Limelight(CougarSystem):
    """Subsystem for interacting with the limelight."""

    def __init__(self):
        super().__init__("limelight")

        self.nt = NetworkTables.getTable("limelight")

        self.driveTable = NetworkTables.getTable("DriveTrain")

        self.setPipeline(1)

        # Grabs the offset.
        constants.limelight.xOffset = (
            self.get("xOffset", constants.limelight.xOffset)
        )
        constants.limelight.yOffset = (
            self.get("yOffset", constants.limelight.yOffset)
        )
        
        constants.limelight.xOffsetStep = self.get('xOffsetStep', constants.limelight.xOffsetStep)
        constants.limelight.yOffsetStep = self.get('yOffsetStep', constants.limelight.yOffsetStep)
        
        self.updateXOffset()
        self.updateYOffset()
        
        self.updateXOffsetStep()
        self.updateYOffsetStep()
        
    def setPipeline(self, pipeline: int):
        """
        Changes the pipeline of the limelight.
        """
        self.put("pipeline", pipeline)

    def setValue(self, name, val):
        """
        Changes any limelight value, given the key and desired val.
        """
        self.put(name, val)

    def getRawY(self):
        """
        Returns the raw x-value, correcting for the limelight rotation.
        """
        return self.get("tx")

    def getY(self):
        """
        Return the x-value to correct for the limelight being rotated.
        """
        return self.get("tx") + constants.limelight.yOffset

    def getRawX(self):
        """
        Returns the raw y-value, correcting for the limelight rotation.
        """
        return self.get("ty") + constants.limelight.xOffset

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
        
    def updateYOffset(self):
        """
        Publish the y-offset to the dashboard.
        """
        self.put('yOffset', constants.limelight.yOffset)
        
    def updateXOffset(self):
        """
        Publish the x-offset to the dashboard.
        """
        self.put('xOffset', constants.limelight.xOffset)
        
    def updateYOffsetStep(self):
        """
        Publish the y-offset step to the dashboard.
        """
        self.put('yOffsetStep', constants.limelight.yOffsetStep)
        
    def updateXOffsetStep(self):
        """
        Publish the x-offset step to the dashboard.
        """
        self.put('xOffsetStep', constants.limelight.xOffsetStep)