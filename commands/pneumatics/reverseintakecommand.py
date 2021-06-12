from commands2 import InstantCommand

import robot


class ReverseIntakeCommand(InstantCommand):

    def __init__(self):
        super().__init__()

        self.addRequirements(robot.pneumatics)


    def initialize(self):
        pass

    def initialize(self):
        robot.pneumatics.retractIntake()
    
    
