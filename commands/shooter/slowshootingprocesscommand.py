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
        self.timerTwo = Timer()

        self.isAtTargetRPM = False

        self.addRequirements([robot.conveyor, robot.chamber])

    def initialize(self):
        self.waiting = False
        
        self.timer.reset()
        
        robot.shooter.setRPM(self.targetRPM)
        self.timer.start()

    def execute(self):
        self.checkRPM()
        
        self.timeReached = self.timer.get() > 3
        
        if self.isAtTargetRPM and self.timeReached:
            # shoot
            robot.conveyor.stop()
            robot.chamber.forward()

            self.timer.stop()            
            self.timer.reset()
            
        elif self.isAtTargetRPM:
            # prep 
            robot.conveyor.forward()
            robot.chamber.stop()
            
            self.timer.start()
            
        else:
            robot.chamber.stop()
            robot.conveyor.forward()
        
                    
    def checkRPM(self):
        if not self.isAtTargetRPM and abs(robot.shooter.getRPM() - self.targetRPM) <= self.tolerance:
            self.isAtTargetRPM = True

    def end(self, interrupted):
        robot.conveyor.stop()
        robot.chamber.stop()
        robot.shooter.stopShooter()
