from commands2 import CommandBase

import robot


class GetColorCommand(CommandBase):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.colorwheel)

    def execute(self):
        self.currentColor = robot.colorwheel.getColor()
        if self.currentColor == "b":
            robot.lights.solidBlue()
        elif self.currentColor == "g":
            robot.lights.solidGreen()
        elif self.currentColor == "y":
            robot.lights.solidYellow()
        elif self.currentColor == "r":
            robot.lights.solidRed()

    def end(self, interrupted):
        print("done color")
