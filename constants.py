from ctre import (
    CANCoderConfiguration,
    AbsoluteSensorRange,
    SensorInitializationStrategy,
)


class Constants:
    """
    Dummy class for robot constants.
    """

    pass


"""
Use this class to declare variables that may have to be 
adjusted a lot. This makes it more global and easier to find. 
Please note that this is not the ports.py. That should host 
IDs for the CANbus, sensors, PWM, and the liking. 
"""

drivetrain = Constants()
shooter = Constants()
limelight = Constants()

# Drive Velocity Control
drivetrain.dPk = 0.0075
drivetrain.dIk = 0
drivetrain.dDk = 1
drivetrain.dFFk = 0.00005
drivetrain.dIZk = 0

# Drive Position Control
drivetrain.sdPk = 0.005  # 0.1
drivetrain.sdIk = 0
drivetrain.sdDk = 0.05
drivetrain.sdFFk = 0.003
drivetrain.sdIZk = 0

# Turn Position Control
drivetrain.tPk = 0.03
drivetrain.tIk = 0
drivetrain.tDk = 0.05
drivetrain.tFFk = 0.005
drivetrain.tIZk = 0

# Turn Secondary Position Control
drivetrain.stPk = 8.5
drivetrain.stIk = 0
drivetrain.stDk = 0
drivetrain.stFFk = 0
drivetrain.stIZk = 0

# The angle of the gyro.
drivetrain.flatAngle = 0

# Gear ratios on the drivetrain.
drivetrain.driveMotorGearRatio = 10.71  # 6.86
drivetrain.turnMotorGearRatio = 12.8

# Motion magic velocities and accelerations
drivetrain.driveMotionAcceleration = 13500
drivetrain.driveMotionCruiseVelocity = 18500
drivetrain.slowDriveMotionCruiseVelocity = 11000

drivetrain.turnMotionAcceleration = 1000
drivetrain.turnMotionCruiseVelocity = 800

# Trajectory constraints.
drivetrain.maxMetersPerSecond = 1  # Velocity for trajectory
drivetrain.maxMetersPerSecondSquared = 0.1  # Accel for trajectory

# Diameter of the wheel in inches.
drivetrain.wheelDiameter = 6
# 6 is correct, 4 provides correct distances, need to figure out why

# Distance between adjacent wheels.
drivetrain.wheelBase = 23.5
drivetrain.trackWidth = 23.5

# Robot width
drivetrain.robotWidth = 27.75

# Center of the robot to the center of a wheel in inches.
drivetrain.robotRadius = 16.84251

drivetrain.speedLimit = (
    30.0  # in inches per second (if you have feet per second, multiply by 12!)
)

drivetrain.encoderConfig = CANCoderConfiguration()
drivetrain.encoderConfig.absoluteSensorRange = AbsoluteSensorRange.Unsigned_0_to_360
drivetrain.encoderConfig.initializationStrategy = (
    SensorInitializationStrategy.BootToAbsolutePosition
)
drivetrain.encoderConfig.sensorDirection = False

drivetrain.mostRecentPath = []  # Updated in record auto.

drivetrain.preBuild = {1: ".barrelracing.json"}

# Constants for the shooter below.

shooter.kP = 0.0018
shooter.kI = 0
shooter.kD = 0.003
shooter.kF = 0.000158
shooter.IZone = 0

# Set the limelight's initial offset values
limelight.xOffset = 0
limelight.yOffset = 0

# Set the step size for modifying the offsets
limelight.xOffsetStep = 0.5
limelight.yOffsetStep = 0.5
