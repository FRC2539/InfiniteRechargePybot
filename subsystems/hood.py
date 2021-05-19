from .cougarsystem import *

import wpilib
import math
import ports

from rev import CANSparkMax, MotorType, ControlType, IdleMode
from custom.config import Config


class Hood(CougarSystem):
    """Controls the robot's hood."""

    def __init__(self):
        super().__init__('Hood')

        # Define the motor object.
        self.motor = CANSparkMax(ports.hood.motorID, MotorType.kBrushless)
        self.motor.setIdleMode(IdleMode.kBrake)
        self.motor.burnFlash()

        # Create the encoder object.
        self.encoder = wpilib.DutyCycle(wpilib.DigitalInput(ports.hood.encoderID))

        # Get the motor's PID controller.
        self.controller = self.motor.getPIDController()

        # Adjust the hood's PID control values.
        self.controller.setP(0.001, 0)
        self.controller.setI(0, 0)
        self.controller.setD(0, 0)
        self.controller.setFF(0, 0)
        self.controller.setIZone(0, 0)

        # The hood's max and min angle.
        self.angleMax = 140.00
        self.angleMin = 65.00

        # The percent to run the hood motor at by default.
        self.speed = 0.3  # 30% percent.

        # Constantly updates the hood's status.
        self.constantlyUpdate("Hood Moving", lambda: self.motor.get() != 0)
        self.constantlyUpdate("Hood Position", self.getPosition)

    def periodic(self):
        """
        Loops when nothing else is running in
        this subsystem. Do not call this!
        """
        self.feed()

    def getPosition(self):
        """
        Returns the position of the hood's encoder
        in degrees, 0-360.
        """
        return self.encoder.getOutput() * 360

    def up(self):
        """
        Raise the hood.
        """
        self.move(self.speed)

    def down(self):
        """
        Lower the hood.
        """
        self.move(-self.speed)

    def move(self, speed):
        """
        Safely moves the hood with a given
        speed.
        """

        if self.isInAngleBounds(speed):
            self.motor.set(speed)
        else:
            self.stop()

    def setShootAngle(self, angle):
        """
        Steven's limelight aiming stuff.
        """
        self.targetpos = self.angleMax - 2 * (angle - 8.84)
        self.error = -1 * (self.getPosition() - self.targetpos)
        if self.angleMin < self.targetpos < self.angleMax:
            if abs(self.error) < 0.1:
                self.stop()
            else:
                self.speed = self.error * 0.01
                if abs(self.speed) > 0.5:
                    self.speed = math.copysign(0.5, self.speed)
                self.motor.set(self.speed)

    def isInAngleBounds(self, speed=0):
        """
        Can the hood move the way you want it to
        (based off of the sign of the speed)? It returns
        true or false depending on if it can move that specific
        direction.
        """
        if speed > 0:
            return self.isUnderMaxAngle()
        elif speed < 0:
            return self.isAboveMinAngle()
        else:
            return self.isUnderMaxAngle() and self.isAboveMinAngle()

    def isUnderMaxAngle(self):
        """
        Is the hood within the max angle?
        """
        return self.getPosition() <= self.angleMax

    def isAboveMinAngle(self):
        """
        Is the hood above the min angle?
        """
        return self.angleMin <= self.getPosition()

    def stop(self):
        """
        Stops the hood motor.
        """
        self.motor.stopMotor()
        self.sendMessage('Hood Stopped!')
