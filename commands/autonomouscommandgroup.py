from wpilib import DriverStation

from commands2 import SequentialCommandGroup, InstantCommand

from commands.drivetrain.turncommand import TurnCommand
from commands.drivetrain.turntocommand import TurnToCommand
from commands.drivetrain.movecommand import MoveCommand

# from commands.limelight.automatedshootcommand import AutomatedShootCommand

from networktables import NetworkTables

import math
import robot, constants

from commands import autoconfig


class AutonomousCommandGroup(SequentialCommandGroup):
    def __init__(self):
        super().__init__()

        ds = DriverStation.getInstance()
        msg = ds.getGameSpecificMessage()

        self.currentAuto = autoconfig.getAutoProgram()
        toRun = self.currentAuto

        for var in dir(self):  # Identifies the method to setup.
            if var.lower() == self.currentAuto:
                toRun = var
                break

        eval("self." + toRun + "()")  # Runs the method

    def example(self):
        """
        Define the function using the name of the autonomous program. It should
        then appear on the driverstation. Put a exclamation point in front of the chosen
        default one! If there is no default selected, the default will be the auto first
        in alphabetical order.
        """
        pass

    def interrupted(self):
        robot.intake.dontIntakeBalls()
        robot.chamber.stop()
        robot.conveyor.stop()
        robot.shooter.stopShooter()

    def shootAndMove(self):
        """
        Shoot 3 balls, then move off the line.
        """
        self.addCommands(
            AutomatedShootCommand(3300),
            MoveCommand(42),
        )
