from commands2 import CommandBase

import robot


class ShootRPMCommand(CommandBase):
    def __init__(self, targetRPM):
        super().__init__()

        self.addRequirements(robot.shooter)

        self.targetRPM = targetRPM

    def initialize(self):
        robot.lights.blinkWhite()

        # Spin up the motor
        robot.shooter.setRPM(self.targetRPM)

    def execute(self):
        # Change the led color if the target rpm has been reached
        if robot.shooter.getRPM() >= self.targetRPM:
            robot.lights.fireRed()
        else:
            robot.lights.blinkWhite()

    def end(self, interrupted):
        # Reset the lights
        robot.lights.rainbow()

        # Stop the shooter
        robot.shooter.stopShooter()
