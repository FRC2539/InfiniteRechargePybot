from wpilib.command import Command

import robot


class ConveyorBackwardCommand(Command):

    def __init__(self):
        super().__init__('Conveyor Backward')

        self.requires(robot.conveyor)


    def initialize(self):
        robot.conveyor.backward()

    def end(self):
        robot.conveyor.stop()
