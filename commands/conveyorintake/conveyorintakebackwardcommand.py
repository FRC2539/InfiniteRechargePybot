from commands2 import CommandBase

import robot


class ConveyorIntakeBackwardCommand(CommandBase):
    """
    Runs the intake and the conveyor in a direction
    that allows balls to reverse through the robot. Remember,
    the intake motor and conveyor systen use the SAME motor
    controller.
    """

    def __init__(self):
        super().__init__()

        self.addRequirements(robot.conveyorintake)

    def initialize(self):
        robot.pneumatics.extendIntake()
        robot.conveyorintake.outtakeBalls()

    def end(self, interrupted):
        robot.pneumatics.retractIntake()
        robot.conveyorintake.stop()
