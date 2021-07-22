from commands2 import InstantCommand

import robot
import constants


class MoveDownOffsetCommand(InstantCommand):
    """
    Adjusts the limelight's return value so that
    it applies a directional correction. In this case,
    it helps the balls head more towards the bottom of the
    powerport.
    """

    def __init__(self):
        super().__init__()

    def initialize(self):
        constants.limelight.yOffset -= constants.limelight.yOffsetStep
        robot.limelight.updateYOffset()
