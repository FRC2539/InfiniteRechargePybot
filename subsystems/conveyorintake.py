from .cougarsystem import *

from wpilib import Timer

import ports
import robot

from ctre import WPI_TalonSRX, NeutralMode, ControlMode


class ConveyorIntake(CougarSystem):
    """Controls the conveyor in the ball system, as well as the intake.
    The conveyor is horizontal and preceeds the chamber. The intake is
    obvious. Both the motor for the intake and the motor for the conveyor
    are on the same motor controller."""

    def __init__(self):
        super().__init__("ConveyorIntake")

        self.motor = WPI_TalonSRX(ports.conveyor.motorID)

        self.motor.setNeutralMode(NeutralMode.Brake)
        self.motor.setInverted(True)

        # INFO: Percentages are from 0 - 1, 1 being 100%
        self.speed = 0.8
        self.slowSpeed = 0.2
        # Option: separate into forward and backward speeds

        # Timer to monitor the intake retraction time.
        self.delayTimer = Timer()
        self.timerWatchdogEnabled = False

        # Delay (in seconds) to pause for after the intake command is stopped.
        self.retractDelay = 1

        # Constantly updates the conveyor's and intake's status.
        self.constantlyUpdate(
            "ConveyorIntake Running", lambda: self.motor.getMotorOutputPercent() != 0
        )

    def periodic(self):
        """
        Loops when nothing else is running in
        this subsystem. Do not call this!
        """
        self.feed()

        if self.timerWatchdogEnabled and self.delayTimer.get() >= self.retractDelay:
            robot.pneumatics.retractIntake()  # Might work.
            self.stop()

            self.resetWatchdog()

    def waitToRetract(self):
        """
        Waits x in seconds to retract the intake. See conveyorintakeforwardcommand.py
        and watchTimer. Watchdog for the timer object. Retracts the intake
        when the time is reached; timer is started by
        waitToRetract.
        """
        self.delayTimer.start()
        self.timerWatchdogEnabled = True
        
    def resetWatchdog(self):
        """
        Resets the watch dog in case it was interrupted or something. 
        For example, this is used when a teleoperator releases the intake button but
        then revives the command before the cooldown is over.
        """
        self.delayTimer.stop()
        self.delayTimer.reset()
        self.timerWatchdogEnabled = False

    def intakeBalls(self):
        """
        Run the conveyor and intake so the balls move
        forwards.
        """
        self.move(self.speed)

    def outtakeBalls(self):
        """
        Reverse the conveyor and intake so the balls
        move backwards.
        """
        self.move(-self.speed)

    def slowIntakeBalls(self):
        """
        Run the conveyor and intake slowly so the balls
        move forward.
        """
        self.move(self.slowSpeed)

    def slowOuttakeBalls(self):
        """
        Run the conveyor and intake slowly so the balls
        move backwards.
        """
        self.move(-self.slowSpeed)

    def move(self, speed):
        """
        Basic move method to set custom speed to the motor.
        """
        self.motor.set(ControlMode.PercentOutput, speed)

    def stop(self):
        """
        Stops the two motors.
        """
        self.motor.stopMotor()
