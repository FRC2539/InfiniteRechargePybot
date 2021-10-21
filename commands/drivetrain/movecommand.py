from commands2 import CommandBase

import robot


class MoveCommand(CommandBase):
    def __init__(self, distance, reversedDirection=False, name=None):
        """
        Takes a distance in inches and stores it for later. We allow overriding
        name so that other autonomous driving commands can extend this class.
        """

        if name is None:
            name = "Move %f inches" % distance

        super().__init__()

        # Determine which direction to drive
        self.reversed = -1 if reversedDirection else 1

        # Calculate the distance to travel
        self.distance = distance * self.reversed

        self.addRequirements(robot.drivetrain)

    def initialize(self):
        # Set the PID profile to the auto one
        # robot.drivetrain.setProfile(1)

        # Store the robot's starting position
        self.startPosition = robot.drivetrain.getPositions()

        # Calculate the target position for the motors
        self.targetPosition = self.startPosition[0] + abs(self.distance)

        # Move forward the given distance
        robot.drivetrain.setPositions(self.distance)

    def isFinished(self):
        positions = robot.drivetrain.getPositions()

        print(self.targetPosition)
        print(min([abs(positions[0]), abs(positions[1])]))

        # Determines if the robot has made it to the target position
        return self.targetPosition <= min([abs(positions[0]), abs(positions[1])])

    def end(self, interrupted):
        # Stop the robot
        robot.drivetrain.stop()

        # Reset the PID profile
        # robot.drivetrain.setProfile(0)
