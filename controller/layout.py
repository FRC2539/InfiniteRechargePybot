from .logitechdualshock import LogitechDualShock
from . import logicalaxes

from custom.config import Config

from commands.drivetrain.drivecommand import DriveCommand
from commands.resetcommand import ResetCommand

from commands.ballintake.intakeforwardcommand import IntakeForwardCommand
from commands.ballintake.intakebackwardcommand import IntakeBackwardCommand

# from commands.hood.RaiseHoodCommand import RaiseHoodCommand
from commands.hood.raisehoodcommand import RaiseHoodCommand
from commands.hood.lowerhoodcommand import LowerHoodCommand

# from commands.shooter.spinupandshootcommand import SpinUpAndShootCommand
# from commands.limelight.automatedshootcommand import AutomatedShootCommand
from commands.limelight.aimwithlimelightcommand import AimWithLimelightCommand

from commands.ballintake.intakeloadcommand import IntakeLoadCommand

from commands.climber.climbupcommand import ClimbUpCommand
from commands.climber.climbdowncommand import ClimbDownCommand


def init():
    """
    Declare all controllers, assign axes to logical axes, and trigger
    commands on various button events. Available event types are:
        - whenPressed
        - whileHeld: cancelled when the button is released
        - whenReleased
        - toggleWhenPressed: start on first press, cancel on next
        - cancelWhenPressed: good for commands started with a different button
    """

    # The controller for driving the robot
    driveController = LogitechDualShock(0)

    logicalaxes.driveX = driveController.LeftX
    logicalaxes.driveY = driveController.LeftY
    logicalaxes.driveRotate = driveController.RightX

    driveController.Back.whenPressed(ResetCommand())
    driveController.X.toggleWhenPressed(DriveCommand())

    driveController.LeftBumper.whileHeld(IntakeLoadCommand())

    driveController.DPadUp.whileHeld(IntakeForwardCommand())
    driveController.DPadDown.whileHeld(IntakeBackwardCommand())

    driveController.DPadRight.whileHeld(RaiseHoodCommand())
    driveController.DPadLeft.whileHeld(LowerHoodCommand())

    driveController.RightBumper.whileHeld(AimWithLimelightCommand())
    # driveController.RightBumper.whileHeld(AutomatedShootCommand(3300))

    driveController.Y.whileHeld(ClimbUpCommand())
    driveController.A.whileHeld(ClimbDownCommand())
