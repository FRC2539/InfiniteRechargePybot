from commands2 import CommandBase

from wpilib import Timer

import robot


class SlowShootingProcessCommand(CommandBase):
    """Gets the shooter up to speed, then moves the ball through the robot and shoot them."""

    def __init__(self, targetRPM=5000, tolerance=50):

        super().__init__()

        self.targetRPM = targetRPM
        self.tolerance = tolerance
        
        self.timer = Timer()

        self.isAtTargetRPM = False

        self.addRequirements([robot.conveyor, robot.chamber])

    def initialize(self):  
        self.timer.stop()
        self.timer.reset()
        
        self.loading = True
        
        robot.shooter.setRPM(self.targetRPM)

        self.timer.start()
        self.goal = 4
        
        self.spotted = False

    def execute(self):
        self.checkRPM()
        
        
        
        # if self.loading and self.goal != 5:
        #     self.goal = 5
                        
        #     robot.chamber.stop()
        #     robot.conveyor.forward()

        # elif not self.loading and self.goal != 3:
        #     self.goal = 3
                        
        #     robot.chamber.forward()
        #     robot.conveyor.stop()
            
        # if self.timer.get() > self.goal:
        #     self.loading = not self.loading
        #     self.timer.reset()
                    
    def checkRPM(self):
        if not self.isAtTargetRPM and abs(robot.shooter.getRPM() - self.targetRPM) <= self.tolerance:
            self.isAtTargetRPM = True

    def end(self, interrupted):
        robot.conveyor.stop()
        robot.chamber.stop()
        robot.shooter.stopShooter()
        
        self.timer.stop()
