#!/usr/bin/env python3

from commands2 import TimedCommandRobot
from wpilib._impl.main import run
from wpilib import RobotBase, DriverStation

from custom import driverhud
import controller.layout
import subsystems
import shutil, sys, os, inspect

from commands2 import Subsystem, CommandScheduler

from commands import autoconfig
from commands.autonomouscommandgroup import AutonomousCommandGroup

from subsystems.monitor import Monitor as monitor
from subsystems.drivetrain import DriveTrain as drivetrain
from subsystems.chamber import Chamber as chamber
from subsystems.conveyorintake import ConveyorIntake as conveyorintake
from subsystems.shooter import Shooter as shooter
from subsystems.limelight import Limelight as limelight
from subsystems.hood import Hood as hood
from subsystems.turret import Turret as turret
from subsystems.pneumatics import Pneumatics as pneumatics


import math


class KryptonBot(TimedCommandRobot):
    """Implements a Command Based robot design"""

    def robotInit(self):
        """Set up everything we need for a working robot."""

        DriverStation.getInstance().silenceJoystickConnectionWarning(True)  # Amen!

        self.subsystems()

        controller.layout.init()
        autoconfig.init()
        driverhud.init()

        self.selectedAuto = autoconfig.getAutoProgram()
        self.auto = AutonomousCommandGroup()

        from commands.drivetrain.zerocancoderscommand import ZeroCANCodersCommand
        from commands.startupcommandgroup import StartUpCommandGroup

        StartUpCommandGroup().schedule()

        from commands.drivetrain.drivecommand import DriveCommand

    def autonomousInit(self):
        """This function is called each time autonomous mode starts."""

        from commands.drivetrain.pathfollowercommand import PathFollowerCommand

        from commands.autonomouscommandgroup import AutonomousCommandGroup

        from commands2 import InstantCommand

        # Send field data to the dashboard
        driverhud.showField()

        # Schedule the autonomous command
        self.auto.schedule()

        driverhud.showInfo("Starting %s" % self.auton)

    def disabledInit(self):
        try:
            self.auton.disable()  # TODO: Fix this.
        except (AttributeError):
            pass

    def disabledPeriodic(self):
        if autoconfig.getAutoProgram() != self.selectedAuto:
            self.selectedAuto = autoconfig.getAutoProgram()
            self.auto = AutonomousCommandGroup()
            print("swapped\n\n")
            # Recreate the auto and its counterparts if the selection changes.

    def handleCrash(self, error):
        super().handleCrash()
        driverhud.showAlert("Fatal Error: %s" % error)

    @classmethod
    def subsystems(cls):
        vars = globals()
        module = sys.modules["robot"]
        for key, var in vars.items():
            try:
                if issubclass(var, Subsystem) and var is not Subsystem:
                    try:
                        setattr(module, key, var())
                    except TypeError as e:
                        print("failed " + str(key))
                        raise ValueError(f"Could not instantiate {key}") from e
            except TypeError:
                pass


def addOutput():
    """
    Creates the array of points for CougarCourses.
    """

    import constants

    from commands.drivetrain.generatevectors import GenerateVectors

    ogOut = sys.stdout

    with open(os.path.dirname(__file__) + "/trajectorydata.txt", "w") as f:

        for id_, file_ in constants.drivetrain.preBuild.items():
            calculatedPoints = GenerateVectors().generate(file_)

            calculatedPoints.insert(0, id_)

            sys.stdout = f

            for point in calculatedPoints:
                print(point)

            print("|||")  # Used to signify the end of a set of points.

        sys.stdout = ogOut

        f.close()


if __name__ == "__main__":
    if len(sys.argv) > 2 and "-g" in sys.argv:
        addOutput()
        sys.argv.remove("-g")

    if len(sys.argv) > 1 and sys.argv[1] == "deploy":
        shutil.rmtree("opkg_cache", ignore_errors=True)
        shutil.rmtree("pip_cache", ignore_errors=True)

    run(KryptonBot)
