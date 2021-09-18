from .cougarsystem import *

import math

# from ctre import ControlMode, NeutralMode, WPI_TalonFX, FeedbackDevice
from ctre import (
    ControlMode,
    NeutralMode,
    WPI_TalonFX,
    TalonFXControlMode,
    TalonFXSensorCollection,
    TalonFXPIDSetConfiguration,
    TalonFXFeedbackDevice,
    Orchestra,
    FeedbackDevice,
)

from navx import AHRS

from custom.config import Config
import ports
import constants


class BaseDrive(CougarSystem):
    """
    A general case drive train system. It abstracts away shared functionality of
    the various drive types that we can employ. Anything that can be done
    without knowing what type of drive system we have should be implemented here.
    """

    def __init__(self, name):
        super().__init__(name)

        """
        Create all motors, disable the watchdog, and turn off neutral braking
        since the PID loops will provide braking.
        """
        try:
            self.motors = [
                WPI_TalonFX(ports.drivetrain.frontLeftMotorID),
                WPI_TalonFX(ports.drivetrain.frontRightMotorID),
                WPI_TalonFX(ports.drivetrain.backLeftMotorID),
                WPI_TalonFX(ports.drivetrain.backRightMotorID),
            ]

        except AttributeError:
            self.motors = [
                WPI_TalonFX(ports.drivetrain.leftMotorID),
                WPI_TalonFX(ports.drivetrain.rightMotorID),
            ]

        for motor in self.motors:
            motor.setNeutralMode(NeutralMode.Brake)
            motor.setSafetyEnabled(False)
            motor.configSelectedFeedbackSensor(FeedbackDevice.IntegratedSensor, 0, 0)

        # Set general names for drivetrain specific functions
        self.move = self.move
        self.resetPID = self.resetPID
        self.setPositions = self.gyroSetPositions
        self.setProfile = self.setProfile
        self.stop = self.stop
        self.inchesToUnits = self.inchesToTicks
        self.getPositions = self.getPositions
        self.averageError = self.averageError
        self.resetEncoders = self.resetEncoders
        self.getVelocity = self.getVelocity
        self.gyroSetPositon = self.gyroSetPositions
        self.unitsToInches = self.ticksToInches

        """
        Subclasses should configure motors correctly and populate activeMotors.
        """
        self.activeMotors = []
        self._configureMotors()

        """Initialize the navX MXP"""
        self.navX = AHRS.create_spi()
        self.resetGyro()
        self.flatAngle = 0
        self.startAngle = self.getAngle()
        self.killMoveVar = 1

        """A record of the last arguments to move()"""
        self.lastInputs = None

        # disablePrint()

        # try:
        # self.folderSong = '/home/lvuser/py/subsystems'
        # print('loaded' + str(self.bensGloriousOrchestra.loadMusic(self.folderSong + '/' + 'song.chrp')))
        # except:
        # print('failed to load orchestra')

        self.turnSet = False
        self.turnDone = False

        self.moveSet = False
        self.moveDone = False

        self.setUseEncoders(True)
        # self.maxSpeed = 16250  # Config('DriveTrain/maxSpeed', 1)
        # self.speedLimit = 16250  # Config('DriveTrain/normalSpeed')
        self.maxSpeed = 8250  # Config('DriveTrain/maxSpeed', 1)
        self.speedLimit = 8250  # Config('DriveTrain/normalSpeed')
        self.deadband = Config("DriveTrain/deadband", 0.05)
        self.maxPercentVBus = 1  # used when encoders are not enabled in percent.

        """Allow changing CAN Talon settings from dashboard"""
        self._publishPID("Speed", 0)
        self._publishPID("Position", 1)

        """Add items that can be debugged in Test mode."""
        # self.debugSensor("navX", self.navX)

        # self.debugMotor("Front Left Motor", self.motors[0])
        # self.debugMotor("Front Right Motor", self.motors[1])

        self.resetEncoders()
        self.resetPID()

        self.setProfile(0)

        # try:
        #     self.debugMotor("Back Left Motor", self.motors[2])
        #     self.debugMotor("Back Right Motor", self.motors[3])
        # except IndexError:
        #     pass

        """Initialize the navX MXP"""
        # self.navX = AHRS.create_spi()
        # self.resetGyro()
        # self.flatAngle = constants.drivetrain.flatAngle

        """A record of the last arguments to move()"""
        # self.lastInputs = None

        # self.speedLimit = self.get("Normal Speed", 0.9)  # 45
        # self.deadband = self.get("Deadband", 0.05)

        # self.wheelBase = (
        #    constants.drivetrain.wheelBase
        # )  # These are distances across the robot; horizontal, vertical, diagonal.

        # self.trackWidth = constants.drivetrain.trackWidth
        # self.r = math.sqrt(self.wheelBase ** 2 + self.trackWidth ** 2)

        # self.wheelDiameter = (
        #    constants.drivetrain.wheelDiameter
        # )  # The diamter, in inches, of our driving wheels.
        # self.circ = (
        #    self.wheelDiameter * math.pi
        # )  # The circumference of our driving wheel.

        # self.driveMotorGearRatio = (
        #    constants.drivetrain.driveMotorGearRatio
        # )  # 6.86 motor rotations per wheel rotation (on y-axis).
        # self.turnMotorGearRatio = (
        #    constants.drivetrain.turnMotorGearRatio
        # )  # 12.8 motor rotations per wheel rotation (on x-axis).

        ## Tell the robot to use encoders.
        # self.useEncoders = True

        ## Tell the robot to flip an axis from the controller
        # self.flipY = False

        ## Constantly update various values in network tables
        # self.constantlyUpdate("Tilt", lambda: self.getTilt())
        # self.constantlyUpdate("Angle", lambda: self.getAngle())
        ## self.constantlyUpdate("Speeds", lambda: self.getSpeeds())

    def periodic(self):
        """
        Loops when nothing else is running in
        this subsystem. Do not call this!
        """
        self.feed()

    def initDefaultCommand(self):
        """
        By default, unless another command is running that requires this
        subsystem, we will drive via joystick using the max speed stored in
        Config.
        """
        from commands.drivetrain.drivecommand import DriveCommand

        self.setDefaultCommand(DriveCommand())

    def resetEncoders(self):
        for motor in self.activeMotors:
            motor.configSelectedFeedbackSensor(FeedbackDevice.IntegratedSensor, 0, 0)
            motor.setSelectedSensorPosition(0, 0, 0)

    def getVelocity(self):
        return [
            TalonFXSensorCollection(motor).getIntegratedSensorVelocity()
            for motor in self.activeMotors
        ]

    def move(self, x, y, rotate):
        # print("mooooove")
        # """Turns coordinate arguments into motor outputs."""

        # """
        # Short-circuits the rather expensive movement calculations if the
        # coordinates have not changed.
        # """
        # if [x, y, rotate] == self.lastInputs:
        #     return

        # self.lastInputs = [x, y, rotate]

        # """Prevent drift caused by small input values"""
        # if self.useEncoders:
        #     x = math.copysign(max(abs(x) - self.deadband, 0), x)
        #     y = math.copysign(max(abs(y) - self.deadband, 0), y)
        #     rotate = math.copysign(max(abs(rotate) - self.deadband, 0), rotate)

        # """Flip the y axis"""
        # if self.flipY:
        #     y = -1 * y

        # speeds = self._calculateSpeeds(x, y, rotate)

        # """Prevent speeds > 1"""
        # maxSpeed = 0
        # for speed in speeds:
        #     maxSpeed = max(abs(speed), maxSpeed)

        # if maxSpeed > 1:
        #     speeds = [x / maxSpeed for x in speeds]

        # """Use speeds to feed motor output."""
        # for motor, speed in zip(self.activeMotors, speeds):
        #     motor.set(ControlMode.PercentOutput, speed * self.speedLimit)
        #     # motor.set(ControlMode.Velocity, speed * self.speedLimit)
        #     # print(f"{motor}: {speed * self.speedLimit}")
        """Turns coordinate arguments into motor outputs."""

        # print("\n\ncheck")

        # Short-circuits the rather expensive movement calculations if the
        # coordinates have not changed.
        if [x, y, rotate] == self.lastInputs:
            return

        if [x, y, rotate] == [0, 0, 0]:
            self.stop()
            return

        self.lastInputs = [x, y, rotate]

        """Prevent drift caused by small input values"""
        if self.useEncoders:
            x = math.copysign(max(abs(x) - self.deadband, 0), x)
            y = math.copysign(max(abs(y) - self.deadband, 0), y)
            rotate = math.copysign(max(abs(rotate) - self.deadband, 0), rotate)

        speeds = self._calculateSpeeds(x, y, rotate)

        """Prevent speeds > 1"""
        maxSpeed = 0
        for speed in speeds:
            maxSpeed = max(abs(speed), maxSpeed)

        if maxSpeed > 1:
            speeds = [x / maxSpeed for x in speeds]

        """Use speeds to feed motor output."""

        self.useEncoders = False

        # print(self.getVelocity())

        if self.useEncoders:
            if not any(speeds):
                """
                When we are trying to stop, clearing the I accumulator can
                reduce overshooting, thereby shortening the time required to
                come to a stop.
                """
                for motor in self.activeMotors:
                    motor.setIntegralAccumulator(0, 0, 0)

            for motor, speed in zip(self.activeMotors, speeds):
                # print(speed)
                motor.set(
                    TalonFXControlMode.Velocity, speed * self.maxSpeed
                )  # make this velocity

        else:
            for motor, speed in zip(self.activeMotors, speeds):
                motor.set(ControlMode.PercentOutput, speed * self.maxPercentVBus)

        if [x, y, rotate] == self.lastInputs:
            return

        if [x, y, rotate] == [0, 0, 0]:
            self.stop()
            return

    def gyroSetPositions(self, positions):
        # """
        # Have the motors move to the given positions. There should be one
        # position per active motor. Extra positions will be ignored.
        # """

        # if not self.useEncoders:
        #     raise RuntimeError("Cannot set position. Encoders are disabled.")

        # for motor in self.motors:
        #     motor.set(
        #         TalonFXControlMode.MotionMagic,
        #         self.getModulePosition(False) + self.inchesToTicks(distance),
        #     )
        if not self.useEncoders:
            raise RuntimeError("Cannot set position. Encoders are disabled.")

        diff = (((self.startAngle - self.getAngle()) / 360)) * self.speedLimit

        motorNum = 0

        for motor, position in zip(self.activeMotors, positions):
            motor.selectProfileSlot(1, 0)
            motor.configMotionCruiseVelocity(int(self.speedLimit + diff), 0)
            motor.configMotionAcceleration(int(self.speedLimit), 0)
            motor.set(ControlMode.MotionMagic, position)

    def averageError(self):
        """Find the average distance between setpoint and current position."""
        error = 0
        for motor in self.activeMotors:
            error += abs(
                motor.getClosedLoopTarget(0) - motor.getSelectedSensorPosition(0)
            )

        return error / len(self.activeMotors)

    def atPosition(self, tolerance=10):
        """
        Check setpoint error to see if it is below the given tolerance.
        """
        return self.averageError() <= tolerance

    def stop(self):
        """Disable all motors until set() is called again."""
        for motor in self.activeMotors:
            motor.set(ControlMode.PercentOutput, 0.0)
            # motor.stopMotor() an alternative to a zero speed stop

        self.lastInputs = None

    def setProfile(self, profile):
        """Select which PID profile to use."""
        for motor in self.activeMotors:
            motor.selectProfileSlot(profile, 0)

    def resetPID(self):
        """Set all PID values for profiles 0, 1, and 2."""
        for motor in self.activeMotors:
            motor.configClosedloopRamp(0, 0)

            # Configure the drive PIDs
            motor.config_kP(0, constants.drivetrain.dPk, 0)
            motor.config_kI(0, constants.drivetrain.dIk, 0)
            motor.config_kD(0, constants.drivetrain.dDk, 0)
            motor.config_kF(0, constants.drivetrain.dFFk, 0)
            motor.config_IntegralZone(0, constants.drivetrain.dIZk, 0)

            # Configure the auto/position control PIDs
            motor.config_kP(1, constants.drivetrain.sdPk, 0)
            motor.config_kI(1, constants.drivetrain.sdIk, 0)
            motor.config_kD(1, constants.drivetrain.sdDk, 0)
            motor.config_kF(1, constants.drivetrain.sdFFk, 0)

            # Configure the turning PIDs
            motor.config_kP(2, constants.drivetrain.tPk, 0)
            motor.config_kI(2, constants.drivetrain.tIk, 0)
            motor.config_kD(2, constants.drivetrain.tDk, 0)
            motor.config_kF(2, constants.drivetrain.tFFk, 0)

    def _publishPID(self, table, profile):
        """
        Read the PID value from the first active CAN Talon and publish it to the
        passed NetworkTable.
        """

        table = NetworkTables.getTable("DriveTrain/%s" % table)

        talon = self.activeMotors[0]

        # TODO: If CTRE ever gives us back the ability to query PID values, send
        # them to NetworkTables here. In the meantime, we just persist the last
        # values that were set via NetworkTables

    def resetGyro(self):
        """Force the navX to consider the current angle to be zero degrees."""

        self.setGyroAngle(0)

    def setGyroAngle(self, angle):
        """Tweak the gyro reading."""

        self.navX.reset()
        self.navX.setAngleAdjustment(angle)

    def getAngle(self):
        """Current gyro reading"""

        return self.navX.getAngle() % 360

    def getAngleTo(self, targetAngle):
        """
        Returns the anglular distance from the given target. Values will be
        between -180 and 180, inclusive.
        """
        degrees = targetAngle - self.getAngle()
        while degrees > 180:
            degrees -= 360
        while degrees < -180:
            degrees += 360

        return degrees

    def inchesToTicks(self, inches):
        """
        Convert inches to the robot's understandable 'tick' unit.
        """
        wheelRotations = (
            inches / self.circ
        )  # Find the number of wheel rotations by dividing the distance into the circumference.
        motorRotations = (
            wheelRotations * self.gearRatio
        )  # Find out how many motor rotations this number is.
        return motorRotations * 2048  # 2048 ticks in one Falcon rotation.

    def ticksToInches(self, ticks):
        """
        Convert 'ticks', robot units, to the imperial unit, inches.
        """
        motorRotations = ticks / 2048
        wheelRotations = motorRotations / self.gearRatio
        return (
            wheelRotations * self.circ
        )  # Basically just worked backwards from the sister method above.

    def inchesPerSecondToTicksPerTenth(self, inchesPerSecond):
        """
        Convert a common velocity to falcon-interprettable
        """
        return self.inchesToDriveTicks(inchesPerSecond / 10)

    def ticksPerTenthToInchesPerSecond(self, ticksPerTenth):
        """
        Convert a robot velocity to a legible one.
        """
        return self.driveTicksToInches(ticksPerTenth * 10)

    def resetTilt(self):
        self.flatAngle = self.navX.getPitch()

    def getTilt(self):
        return self.navX.getPitch() - self.flatAngle

    def getAcceleration(self):
        """Reads acceleration from NavX MXP."""
        return self.navX.getWorldLinearAccelY()

    def getSpeeds(self, inInchesPerSecond=True):
        """Returns the speed of each active motors."""
        if inInchesPerSecond:
            return [
                self.ticksPerTenthToInchesPerSecond(motor.getSelectedSensorVelocity())
                for motor in self.activeMotors
            ]

        # Returns ticks per 0.1 seconds (100 mS).
        return [motor.getSelectedSensorVelocity() for motor in self.activeMotors]

    def getPositions(self, inInches=True):
        """Returns the position of each active motor."""
        if inInches:
            return [
                self.ticksToInches(self.getSelectedSensorPosition(0))
                for x in self.activeMotors
            ]
        return [x.getSelectedSensorPosition(0) for x in self.activeMotors]

    def setUseEncoders(self, useEncoders=True):
        """
        Turns on and off encoders. As a side effect, if encoders are enabled,
        the motors will be set to speed mode. Disabling encoders should not be
        done lightly, as many commands rely on encoder information.
        """
        self.useEncoders = useEncoders

    def setSpeedLimit(self, speed):
        """
        Updates the max speed of the drive and changes to the appropriate
        mode depending on if encoders are enabled.
        """

        self.speedLimit = speed

    def _configureMotors(self):
        """
        Make any necessary changes to the motors and populate self.activeMotors.
        """

        raise NotImplementedError()

    def _calculateSpeeds(self, x, y, rotate):
        """Return a speed for each active motor."""

        raise NotImplementedError()
