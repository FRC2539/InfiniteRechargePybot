from .cougarsystem import *

import ports
import wpilib
import math

from rev import CANSparkMax, MotorType, ControlType

from networktables import NetworkTables as nt


class Hood(CougarSystem):
    """Controls the shooter hood."""

    def __init__(self):
        super().__init__("Hood")

        self.motor = CANSparkMax(ports.hood.motorID, MotorType.kBrushless)
        self.encoder = self.motor.getEncoder()
        self.controller = self.motor.getPIDController()

        # self.table = nt.getTable("Hood")

        self.controller.setP(0.001, 0)
        self.controller.setI(0, 0)
        self.controller.setD(0, 0)
        self.controller.setFF(0, 0)
        self.controller.setIZone(0, 0)

        source_ = wpilib.DigitalInput(ports.hood.absoluteThroughbore)
        self.tbEnc = wpilib.DutyCycle(source_)

        self.dir = "u"
        self.setSpeed = 0.3

        self.angleMax = 236.00  # NOTE DO not actually make this 0 and 90. Place-holder only; make like 20, 110
        self.angleMin = 166.00
        self.LLHoodTuner = 13

        self.limelightAngleMatch = 220

        self.zeroNetworkTables()

    def getPosition(self):
        return self.tbEnc.getOutput() * 360

    def upLLHood(self):
        self.LLHoodTuner = self.LLHoodTuner + 0.1

    def downLLHood(self):
        self.LLHoodTuner = self.LLHoodTuner - 0.1

    def stopHood(self):
        self.motor.stopMotor()

    def setPercent(self, speed):
        self.motor.set(speed)

        self.updateNetworkTables(self.getPosition())

    def raiseHood(self):
        if self.getPosition() < self.angleMax:
            self.motor.set(0.1)
        else:
            self.motor.stopMotor()
        self.updateNetworkTables(self.getPosition())

    def lowerHood(self):
        if self.getPosition() > self.angleMin:
            self.motor.set(-0.1)
        else:
            self.motor.stopMotor()
        self.updateNetworkTables(self.getPosition())

    def atHighest(self):
        if self.getPosition() >= self.angleMax:
            self.motor.stopMotor()
            return True
        else:
            return False

    def atLowest(self):
        if self.getPosition() <= self.angleMin:
            self.motor.stopMotor()
            return True
        else:
            return False

    def updateNetworkTables(self, angle=85.00):
        self.put("HoodAngle", round(self.getPosition(), 2))
        self.put("DesiredHoodAngle", round(angle, 2))
        self.put("LaunchAngle", (((self.angleMax - self.getPosition()) / 2) + 8.84))

    def zeroNetworkTables(self):
        self.put("HoodAngle", self.angleMin)
        self.put("DesiredHoodAngle", self.angleMin)
        self.put("LaunchAngle", self.angleMin)

    def OpenLoopSetPos(self, pos):
        self.angle = pos  # give it in terms between min and max as of now, add 85 onto an angle between 0 and 35,
        # multiply that by 2: 85 + (2 * x). THIS WILL WORK
        if (
            abs(self.getPosition() - self.angle) >= 2
        ):  # this way is better, angle will not be negative. 2 degrees of play
            self.rotate = 0.005 * (self.angle - self.getPosition())  # this should work
            self.setPercent(self.rotate)
        else:
            self.stopHood()

        self.updateNetworkTables(self.getPosition())

    def setShootAngle(self, angle):
        self.targetpos = self.angleMax - 2 * (angle - 8.84)
        self.error = -1 * (self.getPosition() - self.targetpos)
        if self.angleMin < self.targetpos < self.angleMax:
            if abs(self.error) < 0.1:
                self.stopHood()
            else:
                self.speed = self.error * 0.01
                if abs(self.speed) > 0.5:
                    self.speed = math.copysign(0.5, self.speed)
                self.setPercent(self.speed)

    def setAngle(self, angle):
        self.targetpos = 260 - (2 * angle)
        self.error = -1 * (self.getPosition() - self.targetpos)
        if self.angleMin < self.targetpos < self.angleMax:
            if abs(self.error) < 0.1:
                self.stopHood()
            else:
                self.speed = self.error * 0.03
                if abs(self.speed) > 0.5:
                    self.speed = math.copysign(0.5, self.speed)
                self.setPercent(self.speed)

    def benSetAngle(self, angle):  # TO 45 FROM 25
        desiredAngle = self.limelightAngleMatch + (
            angle * 2
        )  # Multiply because the encoder gear turns twice per rotation of the hood gear.

        rotations = desiredAngle * 2 * 210  # This is now in rotations of the motor.

        self.controller.setReference(
            rotations, ControlType.kPosition, 0, 0
        )  # If this does not work, use the WPILIB PID Controller.

        return desiredAngle

    def goTo(self, angle):  # angle is the raw encoder value.
        pos = self.getPosition()
        self.motor.set(
            math.copysign(
                max([0.3, (0.75 - max([angle / pos, pos / angle]))]), angle - pos
            )
        )  # Damn, this is hot.

    def getLLHoodTuner(self):
        return self.LLHoodTuner

    def withinBounds(self):
        return self.angleMin <= self.getPosition() <= self.angleMax
