#!/usr/bin/env python3

from commands2 import TimedCommandRobot
from wpilib._impl.main import run
from wpilib import RobotBase, DriverStation

from custom import driverhud, cougarcoursegrapher
import controller.layout
import subsystems, constants
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
from subsystems.climber import Climber as climber
from subsystems.colorwheel import ColorWheel as colorwheel


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
        
        if self.isSimulation():
            cougarcoursegrapher.init()

    def autonomousInit(self):
        """This function is called each time autonomous mode starts."""

        from commands.drivetrain.pathfollowercommand import PathFollowerCommand

        from commands.autonomouscommandgroup import AutonomousCommandGroup

        from commands2 import InstantCommand

        # Send field data to the dashboard
        driverhud.showField()

        from commands.drivetrain.zerogyrocommand import ZeroGyroCommand

        self.auto.schedule()

    def teleopInit(self):
        self.auto.cancel()

    def disabledInit(self):
        self.auto.cancel()

    def disabledPeriodic(self):
        if autoconfig.getAutoProgram() != self.selectedAuto:
            self.selectedAuto = autoconfig.getAutoProgram()
            self.auto = AutonomousCommandGroup()
            print("\n\nAuto Loaded: " + str(self.selectedAuto) + "\n\n")
            # Recreate the auto and its counterparts if the selection changes.

    def handleCrash(self, error):
        super().handleCrash()
        driverhud.showAlert("Fatal Error: %s" % error)

    @classmethod
    def subsystems(cls):
        vars = globals()
        module = sys.modules["robot"]
        driverhud.checkSystem()
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


def graphCougarCourses():
    """
    Graph the Cougar Course equations.
    """

    


if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == "deploy":
        shutil.rmtree("opkg_cache", ignore_errors=True)
        shutil.rmtree("pip_cache", ignore_errors=True)

    run(KryptonBot)
