from commands2 import CommandBase
from subsystems.swervedrive import SwerveDrive
from custom import driverhud
from custom.config import MissingConfigError
import robot


class MoveCommand(CommandBase):
    def __init__(self, distance):
        """
        Takes a distance in inches and stores it for later. We allow overriding
        name so that other autonomous driving commands can extend this class.
        """
        super().__init__()
        print('running move command')
    def initialize(self):
        robot.drivetrain.setProfile(1)
        robot.drivetrain.setPositions(24)
    def isFinished(self):
        if robot.drivetrain.atPosition():
            pass
        return False
    def end(self, interrupted):
        robot.drivetrain.setProfile(0)
        robot.drivetrain.stop()
