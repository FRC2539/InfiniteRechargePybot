from .logitechdualshock import LogitechDualShock
from .thrustmasterjoystick import ThrustmasterJoystick
from . import logicalaxes

from custom.config import Config

from commands.drivetrain.drivecommand import DriveCommand
from commands.drivetrain.togglefieldorientationcommand import (
    ToggleFieldOrientationCommand,
)
from commands.drivetrain.curvecommand import CurveCommand
from commands.drivetrain.zerocancoderscommand import ZeroCANCodersCommand
from commands.drivetrain.setspeedcommand import SetSpeedCommand

from commands.drivetrain.zerogyrocommand import ZeroGyroCommand

from commands.drivetrain.pathcommand import PathCommand

from commands.resetcommand import ResetCommand

from commands.intake.intakecommand import IntakeCommand
from commands.intake.outtakecommand import OuttakeCommand
from commands.intake.slowouttakecommand import SlowOuttakeCommand

from commands.conveyor.conveyorforwardcommand import ConveyorForwardCommand
from commands.conveyor.conveyorbackwardcommand import ConveyorBackwardCommand

from commands.chamber.chamberforwardcommand import ChamberForwardCommand
from commands.chamber.chamberbackwardcommand import ChamberBackwardCommand

from commands.turret.turretlimelightcommand import TurretLimelightCommand

from commands.shooter.setrpmcommand import SetRPMCommand

from commands.hood.raisehoodcommand import RaiseHoodCommand
from commands.hood.lowerhoodcommand import LowerHoodCommand

from commands.limelight.automatedshootcommand import AutomatedShootCommand


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
    driveControllerOne = ThrustmasterJoystick(0)  # The left hand controller
    driveControllerTwo = ThrustmasterJoystick(1)  # The right hand controller

    logicalaxes.forward = driveControllerOne.Y
    logicalaxes.strafe = driveControllerOne.X

    logicalaxes.rotate = driveControllerTwo.X

    driveControllerOne.LeftBottomLeft.whenPressed(ZeroCANCodersCommand())

    driveControllerOne.LeftThumb.toggleWhenPressed(ChamberForwardCommand())
    driveControllerOne.RightThumb.toggleWhenPressed(ChamberBackwardCommand())
    driveControllerOne.BottomThumb.whenPressed(ZeroGyroCommand())

    driveControllerOne.Trigger.whenPressed(
        SetSpeedCommand(False)
    )  # slow speed while trigger is held.
    driveControllerOne.Trigger.whenReleased(SetSpeedCommand())

    driveControllerOne.LeftBottomRight.whileHeld(PathCommand())

    driveControllerTwo.LeftThumb.toggleWhenPressed(ConveyorForwardCommand())
    driveControllerTwo.RightThumb.toggleWhenPressed(ConveyorBackwardCommand())
    driveControllerTwo.BottomThumb.toggleWhenPressed(IntakeCommand())

    driveControllerTwo.LeftTopLeft.whileHeld(RaiseHoodCommand())
    driveControllerTwo.LeftBottomLeft.whileHeld(LowerHoodCommand())

    driveControllerTwo.Trigger.toggleWhenPressed(AutomatedShootCommand())

    # The controller for non-driving subsystems of the robot
    componentController = LogitechDualShock(2)

    logicalaxes.TURRETmOVE = componentController.LeftX

    componentController.Back.whenPressed(ResetCommand())
    componentController.A.toggleWhenPressed(IntakeCommand())
