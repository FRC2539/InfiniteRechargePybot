from .cougarsystem import *

from ctre import WPI_TalonFX, FeedbackDevice, ControlMode, NeutralMode

from networktables import NetworkTables as nt

import ports


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

        # Set the behavior for when both motors are in "neutral", or are not being moved.
        self.shooterMotorOne.setNeutralMode(NeutralMode.Coast)
        self.shooterMotorTwo.setNeutralMode(NeutralMode.Coast)

        # Set the PID configuration.
        self.shooterMotorOne.config_kF(0, 0, 0)  # Ben, no FF! -Ben
        self.shooterMotorOne.config_kP(0, 5, 0)
        self.shooterMotorOne.config_kI(0, 0, 0)
        self.shooterMotorOne.config_kD(0, 1, 0)
        self.shooterMotorOne.config_IntegralZone(0, 0, 0)

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
        self.feed()

        print(self.getRPM())

    def setRPM(self, rpm):
        # With the second motor following the first, no command is needed for the second motor.
        self.shooterMotorOne.set(ControlMode.Velocity, self.rpmToSensor(rpm))

    def setPercent(self, val):
        self.shooterMotorOne.set(ControlMode.PercentOutput, val)

    def reverseShooter(self):
        # Tell the motor to go in reverse (negative percent).
        self.shooterMotorOne.set(ControlMode.PercentOutput, -0.4)

    def stopShooter(self):
        self.shooterMotorOne.stopMotor()

    def rpmToSensor(self, rpm):
        return (rpm * 2048) / 600

    def sensorToRPM(self, units):
        return (units * 600) / 2048

    def getRPM(self):
        # Return the current average RPM of the motor.
        return self.sensorToRPM(self.shooterMotorOne.getSelectedSensorVelocity())


    def initDefaultCommand(self):
        from commands.shooter.defaultcommand import DefaultCommand

        self.setDefaultCommand(DefaultCommand())
