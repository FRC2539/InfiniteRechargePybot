from commands2 import InstantCommand

import robot


class MoveDownOffsetCommand(InstantCommand):

    def __init__(self):
        super().__init__()

    def initialize(self):
        val = robot.limelight.getX() # Yes, the functions should be inverted.
        val += constants.limelight.yOffsetStep # Increase the value so it has to go 
        # down (or left according to the ll) more to compensate.
        robot.limelight.setValue("ty", val)

