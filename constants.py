from ctre import (
    CANCoderConfiguration,
    AbsoluteSensorRange,
    SensorInitializationStrategy,
)


class Constants:
    pass


"""
Use this class to declare variables that may have to be 
adjusted a lot. This makes it more global and easier to find. 
Please note that this is not the ports.py. That should host 
IDs for the CANbus, sensors, PWM, and the liking. 
"""

drivetrain = Constants()

drivetrain.dPk = 0.0085
drivetrain.dIk = 0
drivetrain.dDk = 0
drivetrain.dFFk = 0.25  # 1?
drivetrain.dIZk = 0

drivetrain.sdPk = 0.1
drivetrain.sdIk = 0
drivetrain.sdDk = 0
drivetrain.sdFFk = 0
drivetrain.sdIZk = 0

drivetrain.tPk = 20.05
drivetrain.tIk = 0
drivetrain.tDk = 0.01
drivetrain.tFFk = 0
drivetrain.tIZk = 0

drivetrain.stPk = 0.01
drivetrain.stIk = 0
drivetrain.stDk = 0
drivetrain.stFFk = 0
drivetrain.stIZk = 0

drivetrain.driveMotorGearRatio = 6.86
drivetrain.turnMotorGearRatio = 12.8

drivetrain.driveMotionAcceleration = 12500
drivetrain.driveMotionCruiseVelocity = 14500
drivetrain.slowDriveMotionCruiseVelocity = 11000

drivetrain.turnMotionAcceleration = 1000
drivetrain.turnMotionCruiseVelocity = 800

drivetrain.maxMetersPerSecond = 1  # Velocity for trajectory
drivetrain.maxMetersPerSecondSquared = 0.1  # Accel for trajectory

drivetrain.wheelDiameter = 4

drivetrain.wheelBase = 23.5
drivetrain.trackWidth = 23.5

drivetrain.robotRadius = 16.84251

drivetrain.speedLimit = (
    80.0  # in inches per second (if you have feet per second, multiply by 12!)
)

drivetrain.encoderConfig = CANCoderConfiguration()
drivetrain.encoderConfig.absoluteSensorRange = AbsoluteSensorRange.Unsigned_0_to_360
drivetrain.encoderConfig.initializationStrategy = (
    SensorInitializationStrategy.BootToAbsolutePosition
)
drivetrain.encoderConfig.sensorDirection = False

drivetrain.preBuild = {
    1: [
        [0, 0, 0, 0, 54, 0.25],
        [0, 54, 0.25, -30, 60, 0.25],
        [-30, 60, 0.25, -60, 66, 0.5],
        [-60, 66, 0.5, -60, 234, 0.5],
        [-60, 234, 0.5, -30, 240, 0.25],
        [-30, 240, 0.25, 0, 246, 0.25],
        [0, 246, 0.25, -30, 300, 0.25],
        [-30, 300, 0.25, -60, 270, 0.25],
        [-60, 270, 0.25, -30, 240, 0.25],
        [-30, 240, 0.25, 0, 210, 0.5],
        [0, 210, 0.5, 0, 66, 0.5],
        [0, 66, 0.5, -30, 60, 0.25],
        [-30, 60, 0.25, -60, 54, 0.25],
        [-60, 54, 0.25, -60, 0, 0],
    ],
}
