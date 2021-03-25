from commands2 import CommandBase

import math

import robot

class ExperimentalSegmentFollowerCommand(CommandBase):
    def __init__(self, waypoints: list, startPoint=[0,0], angleTolerance=5, maxSpeed=1, slowSpeed=0.7, deccelerate=False, speedOffset=0, kP=0.0375, startingAngle=None, stopWhenDone=True):
        """
        You start at [0, 0] by default. speedOffset is applied
        to the left hand side of the drivetrain! Note,
        this is not exactly accurate, but it is pretty consistent!
        If you don't wanna correct the heading, leave kP as 0. If 
        you want to correct it relative to zero (instead of the captured 
        starting angle) leave startingAngle as None. Please 
        note that a "True" in the brackets next to the 
        points will mark the next segment, starting at the 
        point you entered as "True", will follow the slow speed!
        """
        super().__init__()

        waypoints.insert(0, startPoint)  # Adds the first point.

        self.addRequirements(robot.drivetrain)

        self.tol = angleTolerance
        self.deccelerate = deccelerate
        self.speedOffset = speedOffset
        self.kP = kP
        self.startingAngle = startingAngle
        self.stopWhenDone = stopWhenDone

        self.maxSpeed = maxSpeed
        self.ogMaxSpeed = maxSpeed
        
        self.slowSpeed = slowSpeed

        self.distances = []
        self.angles = []

        for i in range(len(waypoints)):
            try:
                point, nextPoint = (
                    waypoints[i],
                    waypoints[i + 1],
                )  # Get two consecutive points.
            except (IndexError):
                break

            # Get each point's components.
            pointX, nextPointX = point[0], nextPoint[0]
            pointY, nextPointY = point[1], nextPoint[1]
            
            # Slow down for this segment?
            try:
                slow = point[2]
            except(IndexError):
                slow = False
                
            # Disable the navX offset control?
            try:
                invertTurn = point[3]
                enterAngle = point[4]
                exitAngle = point[5]
            except(IndexError):
                invertTurn = None
                
            # Find the difference between them.
            finalX = nextPointX - pointX
            finalY = nextPointY - pointY
            
            curveData = None

            if finalX == 0 and finalY == 0:  # Same points, continue onto the next pair.
                continue
            
            distance = math.sqrt(finalX ** 2 + finalY ** 2) # Calculate the distance.

            if finalX == 0:
                if nextPointY > pointY:
                    theta = 180
                else:
                    theta = 0

            elif finalY == 0:
                if nextPointX > pointX:
                    theta = 90
                else:
                    theta = -90
            
            # Experimental Part Here.    
            elif finalX == finalY:
                distance = math.pi / 2 * abs(finalX) # Find arc length.
                theta = enterAngle
                
                curveData = [distance, finalX, enterAngle, exitAngle] # Distance, radius, angle to start at, angle to end at.

            else:
                if finalX > 0: # Going to the right
                    theta = ((math.atan2(finalY, finalX) * 180 / math.pi) + 90) % 180
                else: # Going to the left
                    theta = -((math.atan2(finalX, finalY) * 180 / math.pi) % 180)

            if slow:
                distance *= -1

            self.distances.append([distance, curveData])
            self.angles.append(theta)

    def initialize(self):
        robot.drivetrain.setModuleProfiles(1, turn=False)

        self.pointTracker = 0
        
        if self.startingAngle is None:
            self.startingAngle = 0
        else:
            self.startingAngle = robot.drivetrain.getAngle()

        self.startPos = robot.drivetrain.getPositions()

        self.desiredAngle = self.angles[0]
        
        try:
            self.desiredDistance = self.distances[0][0]
        except(TypeError):
            self.desiredDistance = self.distances[0]
        
        self.disableAdjust = False
        
        self.lastDisplacement = self.desiredDistance

        self.pathFinished = False
        self.notRanYet = True
        self.moveSet = False
        self.passed = True

    def execute(self):
        
        robot.drivetrain.setUniformModuleAngle(self.desiredAngle)
                
        if self.atWaypoint(): # Watches to see if we pass the desired waypoint.
            self.passed = True
            robot.drivetrain.stop()
            return
            
        if self.passed: # Have we gone through the waypoint?

            if self.notRanYet:  # Runs once at the waypoint.
                self.maxSpeed = self.ogMaxSpeed
                
                try: # If it can't index them, then it's done.
                    self.desiredAngle = self.angles[self.pointTracker]
                    self.endAngle = self.desiredAngle
                                        
                except(IndexError):
                    print('\nE')
                    self.pathFinished = True
                    return
                
                # Should we adjust with the NavX?
                
                self.desiredDistance = self.distances[self.pointTracker][0]
                
                if self.distances[self.pointTracker][1] is None:
                    self.disableAdjust = False

                else:
                    self.curveData = self.distances[self.pointTracker][1]
                    self.desiredAngle = self.curveData[2] # The entry angle. 
                    self.endAngle = self.curveData[3] # The exit angle.
             
                # Go slow!
                if self.desiredDistance < 0:
                    self.desiredDistance *= -1 # Make it normal again.
                    self.maxSpeed = self.slowSpeed
                
                self.lastDisplacement = self.desiredDistance
                
                self.startPos = robot.drivetrain.getPositions()
                print('updated start')
                
                self.pointTracker += 1
                
                self.moveSet = False
                self.notRanYet = False
                                
            self.count = 0
            if self.count != 4 and not self.moveSet:
                for currentAngle in robot.drivetrain.getModuleAngles():
                    if (
                        abs(currentAngle - self.desiredAngle) < self.tol
                        or abs(currentAngle - self.desiredAngle - 360) < self.tol
                    ):
                        self.count += 1
                    else:
                        continue

            if self.count >= 2:  # All angles aligned.   
                # Add extra speed because the robot can't follow a damn straight line. My need Weaver's heading
                # algo. 
                robot.drivetrain.setSpeeds([self.maxSpeed + self.speedOffset, self.maxSpeed, self.maxSpeed + self.speedOffset, self.maxSpeed])
                self.moveSet = True
                self.passed = False

        else:
            self.moveSet = False
            self.notRanYet = True
            
            if not self.disableAdjust:
                if abs(self.desiredAngle) < 90:
                    speedOffset = robot.drivetrain.getAngleTo(self.startingAngle)*-self.kP
                else:
                    speedOffset = robot.drivetrain.getAngleTo(self.startingAngle)*self.kP
            else:
                speedOffset = 0
                            
            if self.deccelerate:
                if abs(self.desiredDistance - abs(sum(robot.drivetrain.getPositions()) / 4 - sum(self.startPos) / 4)) <= 18: # Slow down when we are about eighteen inches from the goal.
                    robot.drivetrain.setUniformModulePercent(0.25)
                elif abs(self.desiredDistance - abs(sum(robot.drivetrain.getPositions()) / 4 - sum(self.startPos) / 4)) <= 36: 
                    robot.drivetrain.setUniformModulePercent(0.5)
                else:
                    robot.drivetrain.setSpeeds([self.maxSpeed + speedOffset, self.maxSpeed, self.maxSpeed + speedOffset, self.maxSpeed])
            
            else:
                
                robot.drivetrain.setSpeeds([self.maxSpeed + speedOffset, self.maxSpeed, self.maxSpeed + speedOffset, self.maxSpeed])

    def atWaypoint(self):
        count = 0
        for position, start in zip(robot.drivetrain.getPositions(), self.startPos):
            count += 1
            
            print('diff ' + str(abs(abs(position - start) - self.desiredDistance)))
            print('dd ' + str(self.desiredDistance))
            
            if abs(abs(position - start) - self.desiredDistance) < 1:  # 1 inch is the tolerance, or have we passed it?
                print('\nAt Waypoint')
                return True
        
        return False

    def isFinished(self):
        return self.pathFinished

    def end(self, interrupted):
        if self.stopWhenDone:
            robot.drivetrain.stop()
