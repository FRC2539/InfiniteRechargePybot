from .basedrive import BaseDrive
from ctre import ControlMode
from wpilib.drive import RobotDriveBase
import ports


class SkidDrive(BaseDrive):
    """A drive base where all wheels on each side move together."""

    def __init__(self, name):
        super().__init__(name)

    def _configureMotors(self):

        # Only the front motors are active in a skid system.
        self.activeMotors = self.motors[0:2]

        # Have the rear motors follow the front motors
        if len(self.motors) == 4:
            self.motors[2].follow(self.motors[0])
            self.motors[3].follow(self.motors[1])

        # Invert encoders
        for motor in self.activeMotors:
            motor.setSensorPhase(True)

    def _calculateSpeeds(self, x, y, rotate):
        return [y + rotate, -y + rotate]
