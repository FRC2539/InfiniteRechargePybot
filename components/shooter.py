import wpilib
import math
from rev import CANSparkMax, MotorType, ControlType
from custom.config import Config

class Shooter:

    shooterMotor: object
    intakeRunning: bool

    def setup(self):
        self.encoder = self.shooterMotor.getEncoder()
        self.PIDController = self.shooterMotor.getPIDController()

        self.PIDController.setFF(0.00019 ,0)
        self.PIDController.setP(0.0001 ,0)
        self.PIDController.setI(0 ,0)
        self.PIDController.setD(0.001 ,0)
        self.PIDController.setIZone(0 ,0)

        self.encoder.setPositionConversionFactor(1)


    def runPercent(self, percent: int):
        self.shooterMotor.set(percent)

    def runRPM(self, rpm: int):
        self.PIDController.setReference(float(rpm), ControlType.kVelocity, 0, 0)

    def getRPM(self):
        return self.encoder.getVelocity()

    def execute(self):
        pass
