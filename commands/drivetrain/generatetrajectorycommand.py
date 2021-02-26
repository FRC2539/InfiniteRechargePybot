from commands2 import InstantCommand

import robot


class GenerateTrajectoryCommand(InstantCommand):

    def __init__(self):
        super().__init__()

        self.addRequirements(robot.drivetrain)


    def initialize(self):
        pass


