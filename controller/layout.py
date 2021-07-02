from .logitechdualshock import LogitechDualShock
from .thrustmasterjoystick import ThrustmasterJoystick
from . import logicalaxes

from commands2 import InstantCommand

from commands.drivetrain.drivecommand import DriveCommand
from commands.drivetrain.togglefieldorientationcommand import (
    ToggleFieldOrientationCommand,
)
from commands.drivetrain.curvecommand import CurveCommand
from commands.drivetrain.zerocancoderscommand import ZeroCANCodersCommand
from commands.drivetrain.setspeedcommand import SetSpeedCommand
from commands.drivetrain.recordautocommand import RecordAutoCommand
from commands.drivetrain.runautocommand import RunAutoCommand
from commands.drivetrain.dosadocommand import DosadoCommand
from commands.drivetrain.playsongcommand import PlaySongCommand

from commands.drivetrain.zerogyrocommand import ZeroGyroCommand

from commands.drivetrain.pathcommand import PathCommand

from commands.resetcommand import ResetCommand

from commands.conveyorintake.conveyorintakeforwardcommand import (
    ConveyorIntakeForwardCommand,
)
from commands.conveyorintake.conveyorintakebackwardcommand import (
    ConveyorIntakeBackwardCommand,
)

from commands.chamber.chamberforwardcommand import ChamberForwardCommand
from commands.chamber.chamberbackwardcommand import ChamberBackwardCommand

from commands.climber.lowerclimbercommand import LowerClimberCommand
from commands.climber.raiseclimbercommand import RaiseClimberCommand

from commands.turret.turretlimelightcommand import TurretLimelightCommand

from commands.shooter.setrpmcommand import SetRPMCommand
from commands.shooter.slowshootingprocesscommand import SlowShootingProcessCommand

from commands.hood.raisehoodcommand import RaiseHoodCommand
from commands.hood.lowerhoodcommand import LowerHoodCommand

from commands.limelight.automatedslowshootcommand import AutomatedSlowShootCommand
from commands.limelight.automatedshootcommand import AutomatedShootCommand

from commands.pneumatics.toggleintakecommand import ToggleIntakeCommand

import constants
import robot


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

    driveControllerOne.LeftThumb.toggleWhenPressed(ChamberForwardCommand())
    driveControllerOne.RightThumb.toggleWhenPressed(ChamberBackwardCommand())
    driveControllerOne.BottomThumb.whenPressed(ZeroGyroCommand())

    driveControllerOne.Trigger.whenPressed(
        SetSpeedCommand(False)
    )  # Slow speed when pressed.
    driveControllerOne.Trigger.whenReleased(
        SetSpeedCommand(True)
    )  # Fast speed when pressed again.
    
    driveControllerOne.RightTopLeft.whileHeld(RaiseClimberCommand())
    driveControllerOne.RightBottomLeft.whileHeld(LowerClimberCommand())

    driveControllerTwo.LeftThumb.whileHeld(ConveyorIntakeForwardCommand())
    driveControllerTwo.RightThumb.whileHeld(ConveyorIntakeBackwardCommand())
    driveControllerTwo.BottomThumb.whenPressed(ToggleIntakeCommand())

    driveControllerTwo.Trigger.whileHeld(AutomatedShootCommand())

    driveControllerTwo.LeftTopLeft.whileHeld(RaiseHoodCommand())
    driveControllerTwo.LeftBottomLeft.whileHeld(LowerHoodCommand())
    
    driveControllerTwo.LeftBottomMiddle.whileHeld(SetRPMCommand(3700))
    driveControllerTwo.LeftTopMiddle.whileHeld(ConveyorIntakeForwardCommand())
    driveControllerTwo.LeftTopMiddle.whileHeld(ChamberForwardCommand())

    # The controller for non-driving subsystems of the robot
    componentController = LogitechDualShock(2)

    logicalaxes.TURRETmOVE = componentController.LeftX

    componentController.Back.whenPressed(ResetCommand())

    componentController.LeftTrigger.whileHeld(LowerHoodCommand())
    componentController.LeftBumper.whileHeld(RaiseHoodCommand())
    componentController.RightTrigger.whileHeld(AutomatedShootCommand())

    componentController.A.whenPressed(ToggleIntakeCommand())
    componentController.X.whileHeld(ConveyorIntakeForwardCommand())
    componentController.B.whileHeld(ConveyorIntakeBackwardCommand())
