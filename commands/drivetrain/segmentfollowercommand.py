from commands2 import CommandBase

import math

import robot

class SegmentFollowerCommand(CommandBase):
    def __init__(self, waypoints: list, startPoint=[0,0], angleTolerance=5, maxSpeed=1, slowSpeed=0.7, deccelerate=False, speedOffset=0, kP=0.0275, startingAngle=None, stopWhenDone=True):
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
                disableAdjust = point[3]
            except(IndexError):
                disableAdjust = False
                
            # Find the difference between them.
            finalX = nextPointX - pointX
            finalY = nextPointY - pointY

            if finalX == 0 and finalY == 0:  # Same points, continue onto the next pair.
                continue

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

            else:
                if finalX > 0: # Going to the right
                    theta = ((math.atan2(finalY, finalX) * 180 / math.pi) + 90) % 180
                else: # Going to the left
                    theta = -((math.atan2(finalX, finalY) * 180 / math.pi) % 180)
                    
            distance = math.sqrt(finalX ** 2 + finalY ** 2)

            if slow and disableAdjust:
                self.distances.append([distance, True, True]) # dist, speed, adjust
            elif slow:
                self.distances.append([distance, True, False])
            elif disableAdjust:
                self.distances.append([distance, False, True])
            else:
                self.distances.append(distance)
                                
            self.angles.append(theta)
            
        print(self.angles)

    def initialize(self):
        robot.drivetrain.setModuleProfiles(1, turn=False)
        robot.drivetrain.resetEncoders()

        self.pointTracker = 0
        
        # imagine using if/else statements
        self.startingAngle = (self.startingAngle is None) and 0 or robot.drivetrain.getAngle()

        self.startPos = robot.drivetrain.getPositions()

        self.desiredAngle = self.angles[0]
        
        try:
            self.desiredDistance = self.distances[0][0]
            self.isSlow = self.distances[0][1]
        except(TypeError):
            self.desiredDistance = self.distances[0]
            self.isSlow = False
            
        if self.isSlow:
            self.maxSpeed = self.slowSpeed
            
        self.disableAdjust = False
        
        self.lastDisplacement = self.desiredDistance

        self.pathFinished = False
        self.notRanYet = True
        self.moveSet = False
        self.passed = True

        robot.drivetrain.setUniformModuleAngle(self.desiredAngle)
        
        count = 0
        while count < 4: # Wait for all modules to angle.
            count = 0
            for angle in robot.drivetrain.getModuleAngles():
                
                if (
                    abs(angle - self.desiredAngle) < self.tol
                    or abs(angle - self.desiredAngle - 360) < self.tol
                ):
                    count += 1
                else:
                    continue

    def execute(self):
        
        robot.drivetrain.setUniformModuleAngle(self.desiredAngle)
                        
        if self.atWaypoint(): # Watches to see if we pass the desired waypoint.
            self.passed = True
            
        else:
            self.passed = False
            
        if self.passed: # Have we gone through the waypoint?

            if self.notRanYet:  # Runs once at the waypoint.

                self.maxSpeed = self.ogMaxSpeed
                
                try: # If it can't index them, then it's done.
                    
                    self.desiredAngle = self.angles[self.pointTracker]
                    
                except(IndexError):
                    self.pathFinished = True
                    return
                
                # Should we adjust with the NavX?
                try:
                    self.desiredDistance = self.distances[self.pointTracker][0]
                    self.isSlow = self.distances[self.pointTracker][1]
                    self.disableAdjust = self.distances[self.pointTracker][2]
                    
                except(TypeError, IndexError):
                    self.desiredDistance = self.distances[self.pointTracker]
                    self.isSlow = False
                    self.disableAdjust = False
                    
                # Go slow!
                if self.isSlow:
                    self.maxSpeed = self.slowSpeed
                                
                self.startPos = robot.drivetrain.getPositions()
                
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
            
            print(self.maxSpeed)
            
            if self.deccelerate:
                if abs(self.desiredDistance - abs(sum(robot.drivetrain.getPositions()) / 4 - sum(self.startPos) / 4)) <= 18: # Slow down when we are about eighteen inches from the goal.
                    robot.drivetrain.setUniformModulePercent(0.25)
                elif abs(self.desiredDistance - abs(sum(robot.drivetrain.getPositions()) / 4 - sum(self.startPos) / 4)) <= 36: 
                    robot.drivetrain.setUniformModulePercent(0.5)
                else:
                    robot.drivetrain.setSpeeds([self.maxSpeed + speedOffset, self.maxSpeed, self.maxSpeed + speedOffset, self.maxSpeed])
            
            else:
                
                robot.drivetrain.setSpeeds([self.maxSpeed + speedOffset, self.maxSpeed - speedOffset, self.maxSpeed + speedOffset, self.maxSpeed - speedOffset])

    def atWaypoint(self):
        for position, start in zip(robot.drivetrain.getPositions(), self.startPos):
            #if abs(abs(position - start) - self.desiredDistance) < 1:  # 1 inch is the tolerance, or have we passed it?
            # The following works assuming all encoders increase as we move forward.
            print('pos ' + str(position) + ' start ' + str(start) + ' dd ' + str(self.desiredDistance))
            if (self.desiredDistance + start) - position < 1:
                return True
        
        return False

    def isFinished(self):
        return self.pathFinished

    def end(self, interrupted):
        if self.stopWhenDone:
            robot.drivetrain.stop()
