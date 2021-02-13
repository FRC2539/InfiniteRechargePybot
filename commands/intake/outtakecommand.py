from wpilib.command import Command

import robot


class OuttakeCommand(Command):

    def __init__(self):
        super().__init__('Outtake')

        self.requires(robot.intake)

    def initialize(self):
        robot.intake.fastOut()
    
    def end(self):
        robot.intake.dontIntakeBalls()
