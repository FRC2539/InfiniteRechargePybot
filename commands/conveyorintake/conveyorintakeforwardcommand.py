from commands2 import CommandBase

import robot


class ConveyorIntakeForwardCommand(CommandBase):
    """
    Runs the intake and the conveyor in a direction
    that allows balls to pass through the robot. Remember,
    the intake motor and conveyor systen use the SAME motor
    controller.
    """

    def __init__(self):
        super().__init__()

        self.addRequirements(robot.conveyorintake)

    def initialize(self):
        robot.pneumatics.extendIntake()
        robot.conveyorintake.intakeBalls()

    def end(self, interrupted):
        robot.conveyorintake.waitToRetract()
