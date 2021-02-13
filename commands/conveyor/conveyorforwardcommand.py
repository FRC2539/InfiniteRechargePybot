from wpilib.command import Command

import robot


class ConveyorForwardCommand(Command):

    def __init__(self):
        super().__init__('Conveyor Forward')

        self.requires(robot.conveyor)


    def initialize(self):
        robot.conveyor.forward()

    def end(self):
        robot.conveyor.stop()
