from .cougarsystem import *

from ctre import WPI_TalonFX, FeedbackDevice, ControlMode, NeutralMode

from networktables import NetworkTables as nt

import ports
import constants


class Shooter(CougarSystem):
    """Controls the robot's shooter."""

    def __init__(self):
        super().__init__()

        self.table = nt.getTable("Shooter")

        # Initialize the first motor.
        self.shooterMotorOne = WPI_TalonFX(ports.shooter.motorOneID)
        self.shooterMotorOne.configSelectedFeedbackSensor(
            FeedbackDevice.IntegratedSensor, 0, 0
        )

        # Initialize the second motor.
        self.shooterMotorTwo = WPI_TalonFX(ports.shooter.motorTwoID)
        self.shooterMotorTwo.configSelectedFeedbackSensor(
            FeedbackDevice.IntegratedSensor, 0, 0
        )

        # Add the motors to the robot's orchestra.
        self.addOrchestraInstrument(self.shooterMotorOne)
        self.addOrchestraInstrument(self.shooterMotorTwo)

        # Set the behavior for when both motors are in "neutral", or are not being moved.
        self.shooterMotorOne.setNeutralMode(NeutralMode.Coast)
        self.shooterMotorTwo.setNeutralMode(NeutralMode.Coast)

        # Set the PID configuration.
        self.shooterMotorOne.config_kF(0, constants.shooter.kF, 0)  # Ben, no FF! -Ben
        self.shooterMotorOne.config_kP(0, constants.shooter.kP, 0)
        self.shooterMotorOne.config_kI(0, constants.shooter.kI, 0)
        self.shooterMotorOne.config_kD(0, constants.shooter.kD, 0)
        self.shooterMotorOne.config_IntegralZone(0, constants.shooter.IZone, 0)

        # Set the PID configuration.
        self.shooterMotorTwo.config_kF(0, constants.shooter.kF, 0)  # Ben, no FF! -Ben
        self.shooterMotorTwo.config_kP(0, constants.shooter.kP, 0)
        self.shooterMotorTwo.config_kI(0, constants.shooter.kI, 0)
        self.shooterMotorTwo.config_kD(0, constants.shooter.kD, 0)
        self.shooterMotorTwo.config_IntegralZone(0, constants.shooter.IZone, 0)

        # Tell the second motor to follow the behavior of the first motor.
        self.shooterMotorOne.setInverted(True)
        self.shooterMotorTwo.follow(self.shooterMotorOne)

        # Create state variables.
        self.atGoal = False

        # Set the range of velocities.
        self.maxVel = 5800
        self.minVel = 2800

        # Constantly updates the hood's status.
        self.constantlyUpdate(
            "Shooter Running", lambda: self.shooterMotorOne.getMotorOutputPercent() != 0
        )
        self.constantlyUpdate("Shooter RPM", lambda: float(self.getRPM()))

    def periodic(self):
        """
        Loops when nothing else is running in
        this subsystem. Do not call this!
        """
        self.feed()
        
        print(self.getRPM())

    def setRPM(self, rpm):
        """
        Sets the two shooting motors to a given RPM.
        With the second motor following the first,
        no command is needed for the second motor.
        """
        self.shooterMotorOne.set(ControlMode.Velocity, self.rpmToSensor(rpm))

    def setPercent(self, val):
        """
        Sets the two shooter motors to a
        given percent output.
        """
        self.shooterMotorOne.set(ControlMode.PercentOutput, val)

    def stopShooter(self):
        """
        Stops both shooter motors.
        """
        self.shooterMotorOne.stopMotor()

    def rpmToSensor(self, rpm):
        """
        Convert a standard output RPM into
        a tick units for the robot. Please note,
        this is before the gear ratio on the
        shooter, which is not a 1:1.
        """
        return (rpm * 2048) / 600

    def sensorToRPM(self, units):
        """
        Convert a value in tick units into
        a human-comprehendible RPM. Please note,
        this is before the gear ratio on the
        shooter, which is not a 1:1.
        """
        return (units * 600) / 2048

    def getRPM(self):
        """
        Returns the current RPM of the lead motor,
        motorOne.
        """
        return self.sensorToRPM(self.shooterMotorOne.getSelectedSensorVelocity())
