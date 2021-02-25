from .cougarsystem import *

from ctre import WPI_TalonSRX, FeedbackDevice, ControlMode, NeutralMode

import ports

# May need these
import robot
import math


class Turret(CougarSystem):
    """Controls the turret."""

    def __init__(self):
        super().__init__("Turret")

        self.motor = WPI_TalonSRX(ports.turret.motorID)
        self.motor.config_kP(0, 3.9, 0)
        self.motor.config_kI(0, 0, 0)
        self.motor.config_kD(0, 30, 0)
        self.motor.config_kF(0, 0.07, 0)

        self.maxPosition = 13
        self.minPosition = -13

        self.motor.setNeutralMode(NeutralMode.Brake)

        self.motor.configSelectedFeedbackSensor(FeedbackDevice.QuadEncoder, 0, 0)

        self.motor.setSelectedSensorPosition(0, 0, 0)
        
        # Constantly updates the turret's status.
        self.constantlyUpdate('Turret Moving', lambda: self.motor.getMotorOutputPercent() != 0)
        self.constantlyUpdate('Turret Position', self.getPosition)

    def periodic(self):
        self.feed()

    # if speed is greater than 0 and our position is less than max, move. 
   
    # me (kieren) and ben argued about this command for like 5 minutes
    def move(self, speed):
        if (speed > 0 and self.getPosition() >= self.minPosition) or (speed < 0 and self.getPosition() <= self.maxPosition) or self.positionIsInBounds():
            self.motor.set(speed)
        else:
            self.motor.stopMotor()
        
    def positionIsInBounds(self):
        return self.minPosition <= self.getPosition() <= self.maxPosition

    def getPosition(self):
        return self.motor.getSelectedSensorPosition(0)

    def stop(self):
        self.motor.stopMotor()


    def initDefaultCommand(self):
        from commands.turret.defaultcommand import DefaultCommand

        self.setDefaultCommand(DefaultCommand())
