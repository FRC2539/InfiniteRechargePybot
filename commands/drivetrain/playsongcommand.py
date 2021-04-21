from os.path import dirname
from commands2 import CommandBase

import robot


class PlaySongCommand(CommandBase):
    def __init__(self, fileName: str):
        super().__init__()

        self.addRequirements(robot.drivetrain)
        self.fileName = fileName

        robot.drivetrain.loadSong(self.fileName)

    def initialize(self):
        robot.drivetrain.playSong()

    def end(self, interrupted):
        robot.drivetrain.stopSong()
