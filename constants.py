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
    100.0  # in inches per second (if you have feet per second, multiply by 12!)
)

drivetrain.encoderConfig = CANCoderConfiguration()
drivetrain.encoderConfig.absoluteSensorRange = AbsoluteSensorRange.Unsigned_0_to_360
drivetrain.encoderConfig.initializationStrategy = (
    SensorInitializationStrategy.BootToAbsolutePosition
)
drivetrain.encoderConfig.sensorDirection = False

drivetrain.preBuild = {
    1: ".barrelracing.json"
}
    # non-diagonal distance between points = 30 inches
    # 1: [  # Slalom Path
    #     [0, 0, 0.15],
    #     [0, 48, 0.15],
    #     [-69, 48, 0.15],
    #     [-69, 236, 0.15],
    #     [-12, 236, 0.15],
    #     [-12, 296, 0.15],
    #     [-69, 296, 0.15],
    #     [-69, 236, 0.15],
    #     [-12, 236, 0.15],
    #     [-12, 60, 0.15],
    #     [-90, 60, 0.15],
    #     [-90, 0, 0.15],
    # ],
    
    # 2: [
    #     [0,0,.25],
    #     [0,105,.25],
    #     [15, 120, .25],
    #     [30,135, .25 ],
    #     [45, 120, .25],
    #     [60, 105, .25 ],
    #     [45, 90, .25],
    #     [30,75,.25],
    #     [15, 90, .25],
    #     [0,105,.25],
    #     [0,180,.15],
    #     [-30,210,.15],
    #     [-60,180,.15],
    #     [-30,150,.15],
    #     [0,180,.15],
    #     [60,210,.15],
    #     [60,240,.15],
    #     [30,270,.15],
    #     [0,240,.15],
    #     [0,0,.15],
    #     ],
    # 3: [  # Bounce Path
    #     [0, 0, 0.15],
    #     [10, 50, 0.15],
    #     [60, 60, 0.15],
    #     [0, 70, 0.15],
    #     [-10, 80, 0.15],
    #     [-30, 90, 0.15],
    #     [-60, 120, 0.15],
    #     [-30, 150, 0.15],
    #     [60, 150, 0.15],
    #     [-60, 150, 0.15],
    #     [-60, 240, 0.15],
    #     [60, 240, 0.15],
    #     [0, 240, 0.15],
    #     [0, 310, 0.15],
    # ],
    # 4: [  # test
    #     [0, 0, 0.05],
    #     [10, 10, 0.05],
    #     [0, 0, 0.05],
    # ],
# }
