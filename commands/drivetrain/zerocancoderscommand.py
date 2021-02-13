from commands2 import CommandBase

import robot


class ZeroCANCodersCommand(CommandBase):
    def __init__(self, offsets=[-255.9375, -271.9, -41.8, -130.1]):
        super().__init__()

        """
        Used to zero the CANCoders. Ensure all wheels are straight, then 
        call this command. 
        """

        self.addRequirements(robot.drivetrain)

        self.offsets = offsets

    def initialize(self):

        robot.drivetrain.updateCANCoders(self.offsets)

        print("my angles (zeroes)" + str(robot.drivetrain.getModuleAngles()))

    def end(self, interrupted):
        pass
