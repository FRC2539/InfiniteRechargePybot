from .logitechdualshock import LogitechDualShock
from . import logicalaxes

from custom.config import Config

from commands.drivetrain.drivecommand import DriveCommand
from commands.resetcommand import ResetCommand

from commands.ballintake.intakeforwardcommand import IntakeForwardCommand
from commands.ballintake.intakebackwardcommand import IntakeBackwardCommand

from commands.hood.raisehoodcommand import RaiseHoodCommand
from commands.hood.lowerhoodcommand import LowerHoodCommand

from commands.limelight.automatedshootcommand import AutomatedShootCommand

from commands.ballintake.intakeloadcommand import IntakeLoadCommand

from commands.climber.climbupcommand import ClimbUpCommand
from commands.climber.climbdowncommand import ClimbDownCommand
from commands.climber.forceclimbdowncommand import ForceClimbDownCommand

from commands.shooter.shootrpmcommand import ShootRPMCommand
from commands.shooter.spinupandshootcommand import SpinUpAndShootCommand

# from commands.hood.sethoodpositioncommand import SetHoodPositionCommand
from commands.drivetrain.turncommand import TurnCommand
from commands.drivetrain.movecommand import MoveCommand

from commands.colorwheel.spinwheelcommand import SpinWheelCommand
from commands.colorwheel.getcolorcommand import GetColorCommand


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

    # Configure the controller axes
    logicalaxes.driveX = driveController.LeftX
    logicalaxes.driveY = driveController.LeftY
    logicalaxes.driveRotate = driveController.RightX

    driveController.Back.whenPressed(ResetCommand())
    # driveController.X.toggleWhenPressed(DriveCommand())

    # Configure the d pad
    driveController.DPadUp.whileHeld(IntakeForwardCommand())
    driveController.DPadDown.whileHeld(IntakeBackwardCommand())
    driveController.DPadRight.whileHeld(RaiseHoodCommand())
    driveController.DPadLeft.whileHeld(LowerHoodCommand())

    # Configure the bumpers and triggers
    driveController.LeftBumper.whileHeld(IntakeLoadCommand())
    driveController.RightBumper.whileHeld(AutomatedShootCommand(4500))
    # driveController.RightTrigger.whileHeld(ForceClimbDownCommand())
    driveController.LeftTrigger.whileHeld(SpinWheelCommand())

    # Configure the letter buttons
    driveController.Y.whileHeld(ClimbUpCommand())
    driveController.A.whileHeld(ClimbDownCommand())
    driveController.B.whenPressed(TurnCommand(90))
    # driveController.X.whenPressed(MoveCommand(-40))
    driveController.X.whenPressed(GetColorCommand())

    # The controller for operating the robot
    operatorController = LogitechDualShock(1)

    # Configure the letter buttons
    operatorController.Y.whileHeld(ClimbUpCommand())
    operatorController.A.whileHeld(ForceClimbDownCommand())

    # Configure the d pad
    operatorController.DPadUp.whileHeld(IntakeForwardCommand())
    operatorController.DPadDown.whileHeld(IntakeBackwardCommand())

    # Configure the bumpers and triggers
    operatorController.LeftBumper.whileHeld(RaiseHoodCommand())
    operatorController.LeftTrigger.whileHeld(LowerHoodCommand())
    operatorController.RightBumper.whileHeld(ShootRPMCommand(4500))
    operatorController.RightTrigger.whileHeld(SpinUpAndShootCommand(4500))
