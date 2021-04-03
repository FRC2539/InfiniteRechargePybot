from commands2 import CommandBase

from robotpy_ext.misc import NotifierDelay

import math, os, inspect
import robot, constants


class RunAutoCommand(CommandBase):
    def __init__(self, points: list = []):
        """
        Distance is the distance we should travel in inches, turnOffset
        is the angle displacement of the gyro in degrees. Get points
        from the RecordAutoCommand. I recommend running 'black' on the container file
        afterwards format the list if you copy and paste from the terminal.
        """

        super().__init__()

        self.addRequirements([robot.drivetrain])

        self.points = points

    def initialize(self):
        if self.points == []:
            self.points = constants.drivetrain.mostRecentPath

        robot.drivetrain.setModuleProfiles(0, drive=False)

        self.cycleCount = 0
        self.done = False

    def execute(self):
        with NotifierDelay(0.01) as delay:
            try:
                robot.drivetrain.setPercents(self.points[self.cycleCount][0])
                print("angles " + str(self.points[self.cycleCount][1]))
                robot.drivetrain.setModuleAngles(self.points[self.cycleCount][1])
            except (IndexError):
                self.done = True
            self.cycleCount += 1
            delay.wait()

    def isFinished(self):
        return self.done

    def end(self, interrupted):
        print("\n\nEnd\n\n")
        robot.drivetrain.stop()
