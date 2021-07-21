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

        # Standard speed of the climber, up and down.
        self.speed = 1
        self.slowSpeed = 0.5

        # Climber limits.
        self.upperLimit = 515000
        self.lowerLimit = 14000  # Give some wiggle room.

    def periodic(self):
        """
        Loops when nothing else is running in
        this subsystem. Do not call this!
        """
        self.feed()

    def raiseClimber(self):
        """
        Raises the climber using the climber motor.
        """
        if not self.atUpperLimit():
            self.climberMotor.set(self.speed)
        else:
            self.stopClimber()

    def lowerClimber(self):
        """
        Lowers the climber using the climber motor.
        """
        if not self.atLowerLimit():
            self.climberMotor.set(-self.speed)
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
