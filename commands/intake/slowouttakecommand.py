from wpilib.command import Command

import robot


class SlowOuttakeCommand(Command):

    def __init__(self):
        super().__init__('Slow Outtake')

        self.requires(robot.intake)

    def initialize(self):
        robot.intake.slowOut()

    def end(self):
        robot.intake.dontIntakeBalls()
