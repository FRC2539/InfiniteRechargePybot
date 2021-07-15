from commands2 import InstantCommand

import robot


class MoveRightOffsetCommand(InstantCommand):
    def __init__(self):
        super().__init__()

    def initialize(self):
        val = robot.limelight.getY()  # Yes, the functions should be inverted.
        val += constants.limelight.xOffsetStep  # Increase the value so it has to go
        # right (or down according to the ll) more to compensate.
        robot.limelight.setValue("tx", val)
