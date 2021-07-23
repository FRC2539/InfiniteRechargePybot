from .cougarsystem import CougarSystem

from ctre import WPI_TalonFX, NeutralMode, FeedbackDevice

import ports
import math


class Climber(CougarSystem):
    """Describe what this subsystem does."""

    def __init__(self):
        super().__init__("Climber")

        # The motor and it's modifications.
        self.climberMotor = WPI_TalonFX(ports.climber.motorID)

        self.climberMotor.setNeutralMode(NeutralMode.Brake)
        self.climberMotor.setSafetyEnabled(False)
        self.climberMotor.setInverted(False)

        self.climberMotor.configSelectedFeedbackSensor(
            FeedbackDevice.IntegratedSensor, 0, 0
        )
        self.climberMotor.setSelectedSensorPosition(
            0
        )  # Start at zero so we don't risk over-driving downwards.

        # Pulley radius, in inches. NOTE: this is a guess lol.
        self.pulleyRadius = 1.5

        # Standard speed of the climber, up and down.
        self.speed = 1
        self.slowSpeed = 0.5
        self.fallingSpeedDeadband = 250  # NOTE: Measure this.

        # Climber limits.
        self.upperLimit = 515000
        self.lowerLimit = 14000  # Give some wiggle room.

        # A boolean used to represent the status of the climber.
        self.climbing = False
        self.climberMoving = False

        # The locked status of the climber.
        self.put("locked", False)

    def periodic(self):
        """
        Loops when nothing else is running in
        this subsystem. Do not call this!
        """
        self.feed()
        self.hasLocked()

        print(
            str(self.climbing)
            + " "
            + str(self.climberMotor.getSelectedSensorPosition() < 0.2 * self.upperLimit)
            + " "
            + str(not self.climberMoving)
            + " "
            + str(not self.isFalling())
        )  # Test this.

    def raiseClimber(self):
        """
        Raises the climber using the climber motor.
        """
        if not self.atUpperLimit():
            self.climberMotor.set(self.speed)
            self.climberMoving = True
        else:
            self.stopClimber()

    def lowerClimber(self):
        """
        Lowers the climber using the climber motor.
        """
        if not self.atLowerLimit():
            self.climberMotor.set(-self.speed)
            self.climberMoving = True
        else:
            self.stopClimber()

    def forceLowerClimber(self):
        """
        Oh boy; daring are we?
        """
        self.climberMotor.set(-self.slowSpeed)

    def stopClimber(self):
        """
        Stops the climber motor.
        """
        self.climberMotor.stopMotor()
        self.climberMoving = False

    def atUpperLimit(self):
        """
        Returns true if the integrated encoder says we have
        reached our max height limit.
        """
        return self.climberMotor.getSelectedSensorPosition() >= self.upperLimit

    def atLowerLimit(self):
        """
        Returns true if the integrated encoder says we have
        reached our lower limit (if the climber is lowered
        all the way; ideally, we shouldn't need this).
        """
        return self.climberMotor.getSelectedSensorPosition() <= self.lowerLimit

    def hasLocked(self):
        """
        Updates the "locked" value, which represents
        the status of the climber's locking mechanism.
        It assumes the status by watching the encoder.
        """
        # If we are more than 70% up, begin looking for signs of climbing.
        if self.climberMotor.getSelectedSensorPosition() > 0.7 * self.upperLimit:
            self.climbing = True
        # If we have raised and begun to lower our climber, we're watching. If the climber
        # is not being told to move, and we are not slowly falling, we're safe.
        elif (
            self.climbing  # We have gone up then down.
            and self.climberMotor.getSelectedSensorPosition()
            < 0.2 * self.upperLimit  # We are at the bottom.
            and not self.climberMoving  # The climber is not being moved by a command.
            and not self.isFalling()  # The climber is not falling.
        ):  # If all of this is true, we are locked.
            self.put("locked", True)

    def isFalling(self):
        """
        Watches the speed of the climber. If it slowl and negative, it
        assumes we are falling. We provide a falling speed so that we can allow
        for minor errors in our calculations. So basically this returns true
        if we are falling faster than the fallingSpeedDeadband.
        """
        return abs(
            self.climberMotor.getSelectedSensorVelocity() > self.fallingSpeedDeadband
        )  # Return true if we are falling.
