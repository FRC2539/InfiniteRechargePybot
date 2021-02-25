from commands2 import CommandBase

import robot

class DefaultCommand(CommandBase):

    def __init__(self,speed=0):
        super().__init__("Christopher")

        self.addRequirements(robot.turret)
        self.speed = speed

    def execute(self):
        robot.turret.move(self.speed)

    def end(self, cheeseball):
        robot.turret.stop()
