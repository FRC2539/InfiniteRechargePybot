from wpilib.command.command import Command

import robot

class DeelevateCommand(Command):

    def __init__(self):
        super().__init__('Deelevate')

        self.requires(robot.elevator)


    def initialize(self):
        self._finished = False


    def execute(self):
        self._finished = robot.elevator.down()
        print(robot.elevator.getPosition())

    def isFinished(self):
        return self._finished


    def end(self):
        robot.elevator.stop()
