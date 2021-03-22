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
        
        self.movingPhase = 0
        self.lastWait = 0

        self.isAtTargetRPM = False

        self.addRequirements([robot.conveyor, robot.chamber])
        
    def checkRPM(self):
        return abs(robot.shooter.getRPM() - self.targetRPM) <= self.tolerance
        
    def initialize(self):
        self.timer.stop()
        self.timer.reset()
        
        robot.shooter.setRPM(self.targetRPM)
        
        self.timer.start()
        
    def the(self):
        robot.chamber.stop()
        robot.conveyor.forward()
    
    def execute(self):
        if self.movingPhase == 0:
            if self.timer.get() > 1.5 and self.timer.get() > self.lastWait+.5:
                self.lastWait = self.timer.get()
                atTarget = self.checkRPM()
                
                if atTarget:
                    robot.chamber.forward()
                    robot.conveyor.stop()
                    self.movingPhase = 1
                    
                else:
                    self.the()
                    
            else:
                self.the()
                
        elif self.movingPhase == 1:
            if robot.chamber.isBallPresent() == True:
                self.movingPhase = 2
                
        elif self.movingPhase == 2:
            if robot.chamber.isBallPresent() != True:
                self.movingPhase = 0
                self.the()
        
    
    def end(self,interrupted):
        robot.conveyor.stop()
        robot.chamber.stop()
        robot.shooter.stopShooter()
        
        self.timer.stop()
        
        
'''
    def initialize(self):  
=======
    def initialize(self):
>>>>>>> 629c1359dab3ebc5a6415b248b61f92a69af0bfa
        self.timer.stop()
        self.timer.reset()

        self.loading = True

        robot.shooter.setRPM(self.targetRPM)

        self.timer.start()
        self.goal = 2.25

    def execute(self):
        self.checkRPM()

        if self.loading and self.goal != 2.25:
            self.goal = 2.25

            robot.chamber.stop()
            robot.conveyor.forward()

        elif not self.loading and self.goal != 1.25:
            self.goal = 1.25

            robot.chamber.forward()
            robot.conveyor.stop()

        if self.timer.get() > self.goal:
            self.loading = not self.loading
            self.timer.reset()

    def checkRPM(self):
        if (
            not self.isAtTargetRPM
            and abs(robot.shooter.getRPM() - self.targetRPM) <= self.tolerance
        ):
            self.isAtTargetRPM = True

    def end(self, interrupted):
        robot.conveyor.stop()
        robot.chamber.stop()
        robot.shooter.stopShooter()

        self.timer.stop()
'''
