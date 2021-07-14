from commands2 import InstantCommand

import robot


class MoveUpOffsetCommand(InstantCommand):

    def __init__(self):
        super().__init__()

    def initialize(self):
        val = robot.limelight.getX() # Yes, the functions should be inverted.
        val -= constants.limelight.yOffsetStep # Decrease the value so it has to go 
        # up (or right according to the ll) more to compensate.
        robot.limelight.setValue("ty", val)


