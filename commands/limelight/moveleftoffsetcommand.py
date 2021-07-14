from commands2 import InstantCommand

import robot
import constants

class MoveLeftOffsetCommand(InstantCommand):

    def __init__(self):
        super().__init__()

    def initialize(self):
        val = robot.limelight.getY() # Yes, the functions should be inverted.
        val -= constants.limelight.xOffsetStep # Decrease the value so it has to go 
        # left (or up according to the ll) more to compensate.
        robot.limelight.setValue("tx", val)

