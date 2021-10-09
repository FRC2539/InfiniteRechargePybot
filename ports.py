"""
This is the place where we store port numbers for all subsystems. It is based on
the RobotMap concept from WPILib. Each subsystem should have its own ports list.
Values other than port numbers should be stored in Config.
"""


class PortsList:
    """Dummy class used to store variables on an object."""

    pass


hood = PortsList()

hood.motorID = 10
hood.absoluteThroughbore = 0  # DI/O

lights = PortsList()
lights.lightControllerID = 0  # PWM

drivetrain = PortsList()

"""CAN IDs for motors"""
drivetrain.frontLeftMotorID = 4
drivetrain.frontRightMotorID = 1
drivetrain.backLeftMotorID = 3
drivetrain.backRightMotorID = 2

ballintake = PortsList()

"""IDs for ball intake"""
ballintake.intakeMotor = 5
ballintake.conveyorMotor = 7
ballintake.shooterFeedMotor = 6

ballintake.intakeSensor = 0
ballintake.conveyorSensor = 1
ballintake.shooterSensor = 2

shooter = PortsList()
"""IDs for shooter motors"""

shooter.leadMotor = 8
shooter.followMotor = 9

limelight = PortsList()

climber = PortsList()
climber.motor = 11

colorWheelSpinner = PortsList()

colorWheelSpinner.motor = 12
colorWheelSpinner.sensor = 0  # I2C port
