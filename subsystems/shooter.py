from .cougarsystem import *

import ports
import constants

from rev import CANSparkMax, ControlType, MotorType, IdleMode


class Shooter(CougarSystem):
    """
    Controls the shooter.
    """

    def __init__(self):
        super().__init__("Shooter")

        # Initialize the lead motor for the shooter
        self.leadMotor = CANSparkMax(ports.shooter.leadMotor, MotorType.kBrushless)
        self.leadEncoder = self.leadMotor.getEncoder()
        self.leadPIDController = self.leadMotor.getPIDController()

        # Initialize the follow motor
        self.followMotor = CANSparkMax(ports.shooter.followMotor, MotorType.kBrushless)
        self.followEncoder = self.leadMotor.getEncoder()
        self.followPIDController = self.leadMotor.getPIDController()

        # Have the follow motor follow the lead motor but reversed
        self.followMotor.follow(self.leadMotor, True)

        # Set PID values for the lead motor
        self.leadPIDController.setFF(constants.shooter.kF, 0)
        self.leadPIDController.setP(constants.shooter.kP, 0)
        self.leadPIDController.setI(constants.shooter.kI, 0)
        self.leadPIDController.setD(constants.shooter.kD, 0)
        self.leadPIDController.setIZone(constants.shooter.IZone, 0)

        # Set PID values for the follow motor
        self.followPIDController.setFF(constants.shooter.kF, 0)
        self.followPIDController.setP(constants.shooter.kP, 0)
        self.followPIDController.setI(constants.shooter.kI, 0)
        self.followPIDController.setD(constants.shooter.kD, 0)
        self.followPIDController.setIZone(constants.shooter.IZone, 0)

        # Set both motors to coast when idle
        self.leadMotor.setIdleMode(IdleMode.kCoast)
        self.followMotor.setIdleMode(IdleMode.kCoast)

        # Constantly updates the shooter's status
        # in NetworkTables.
        self.constantlyUpdate("Shooter Running", lambda: self.leadMotor.get() != 0)
        self.constantlyUpdate("Shooter RPM", lambda: float(self.getRPM()))

    def periodic(self):
        """
        Loops when nothing else is running in
        this subsystem. Do not call this!
        """
        self.feed()

    def setRPM(self, rpm):
        """
        Sets the two shooting motors to a given RPM.
        With the second motor following the first,
        no command is needed for the second motor.
        """
        self.leadPIDController.setReference(float(rpm), ControlType.kVelocity, 0, 0)

    def setPercent(self, val):
        """
        Sets the shooter motors to a given percent output.
        """
        self.leadMotor.set(val)

    def stopShooter(self):
        """
        Stops both shooter motors.
        """
        self.leadMotor.stopMotor()

    def getRPM(self):
        """
        Returns the current RPM of the lead motor.
        """
        return self.leadEncoder.getVelocity()
