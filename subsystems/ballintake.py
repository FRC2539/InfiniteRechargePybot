from .cougarsystem import *

import ports

from wpilib import AnalogInput

from ctre import WPI_TalonSRX, NeutralMode, ControlMode


class BallIntake(CougarSystem):
    """
    Controls the full ball intake system within the robot.
    """

    def __init__(self):
        super().__init__("BallIntake")

        # Intialize the motor objects
        self.motors = {}

        self.motors["intakeMotor"] = WPI_TalonSRX(ports.ballintake.intakeMotor)
        self.motors["conveyorMotor"] = WPI_TalonSRX(ports.ballintake.conveyorMotor)
        self.motors["shooterFeedMotor"] = WPI_TalonSRX(
            ports.ballintake.shooterFeedMotor
        )

        # Configure the ball intake motors
        for motor in self.motors:
            self.motors[motor].setNeutralMode(NeutralMode.Brake)

        self.motors["conveyorMotor"].setInverted(True)
        self.motors["shooterFeedMotor"].setInverted(True)

        # Percentages are from 0 - 1, 1 being 100%
        self.speeds = {
            "intakeMotor": 0.4,
            "conveyorMotor": 0.55,
            "shooterFeedMotor": 0.75,  # 0.9
        }

        # Initialize the analog inputs for checking if a ball is present
        self.intakeSensor = AnalogInput(ports.ballintake.intakeSensor)
        self.conveyorSensor = AnalogInput(ports.ballintake.conveyorSensor)

        # Set a threshold for confirming a ball's presence
        self.ballPresentThreshold = 50

        # Constantly updates the intake's status.
        self.constantlyUpdate(
            "Ball Intake Running",
            lambda: self.motors["intakeMotor"].getMotorOutputPercent() != 0,
        )

    def periodic(self):
        """
        Loops when nothing else is running in
        this subsystem. Do not call this!
        """
        self.feed()

    def forwardIntake(self):
        """
        Runs the intake motor forward
        """
        self.forwardMotor("intakeMotor")

    def forwardConveyor(self):
        """
        Runs the conveyor motor forward
        """
        self.forwardMotor("conveyorMotor")

    def forwardShooterFeed(self):
        """
        Runs the shooter feed motor forward
        """
        self.forwardMotor("shooterFeedMotor")

    def stopIntake(self):
        """
        Stops the intake motor
        """
        self.stopMotor("intakeMotor")

    def stopConveyor(self):
        """
        Stops the conveyor motor
        """
        self.stopMotor("conveyorMotor")

    def stopShooterFeed(self):
        """
        Stops the shooter feed motor
        """
        self.stopMotor("shooterFeedMotor")

    def forwardAll(self):
        """
        Run the ball intake system so the balls move
        forwards.
        """
        for motor in self.motors:
            self.forwardMotor(motor)

    def backwardAll(self):
        """
        Reverse the ball intake system so the balls
        move backwards.
        """
        for motor in self.motors:
            self.backwardMotor(motor)

    def stopAll(self):
        """
        Stops the ball intake system.
        """
        for motor in self.motors:
            self.stopMotor(motor)

    def forwardMotor(self, motor):
        """
        Run a specific motor forward.
        """
        self.moveMotor(self.motors[motor], self.speeds[motor])

    def backwardMotor(self, motor):
        """
        Run a specific motor backward.
        """
        self.moveMotor(self.motors[motor], -self.speeds[motor])

    def moveMotor(self, motor, speed):
        """
        Basic move method to set custom speed to a motor.
        """
        motor.set(ControlMode.PercentOutput, speed)

    def stopMotor(self, motor):
        """
        Stop a specific motor
        """
        self.motors[motor].stopMotor()

    def isIntakeBallPresent(self):
        """
        Checks if the ball is present in the intake
        """
        return self.intakeSensor.getValue() < self.ballPresentThreshold

    def isConveyorBallPresent(self):
        """
        Checks if the ball is present in the conveyor
        """
        return self.conveyorSensor.getValue() < self.ballPresentThreshold
