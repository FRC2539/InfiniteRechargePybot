from .cougarsystem import *

import ports

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
            "intakeMotor": 1,
            "conveyorMotor": 1,
            "shooterFeedMotor": 1,
        }

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
