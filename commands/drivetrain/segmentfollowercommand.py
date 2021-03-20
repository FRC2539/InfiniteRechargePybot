from commands2 import CommandBase

import math

import robot

class SegmentFollowerCommand(CommandBase):
    def __init__(self, waypoints: list, angleTolerance=5):
        """
        You start at [0, 0].
        """
        super().__init__()

        waypoints.insert(0, [0, 0])  # Adds the first point.

        self.addRequirements(robot.drivetrain)

        self.tol = angleTolerance

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
                    print('here')
                    theta = ((math.atan2(finalY, finalX) * 180 / math.pi) + 90) % 180
                else: # Going to the left
                    theta = -((math.atan2(finalY, finalX) * 180 / math.pi) % 180)
                    
            print('THETA ' + str(theta))

            distance = math.sqrt(finalX ** 2 + finalY ** 2)

            self.distances.append(distance)
            self.angles.append(theta)
        
        print(self.distances)
        print(self.angles)

    def initialize(self):
        robot.drivetrain.setModuleProfiles(1, turn=False)

        self.pointTracker = 0

        self.startPos = robot.drivetrain.getPositions()

        self.desiredAngle = self.angles[0]
        self.desiredDistance = self.distances[0]

        self.pathFinished = False
        self.notRanYet = True
        self.moveSet = False
        self.passed = True

    def execute(self):
        
        robot.drivetrain.setUniformModuleAngle(self.desiredAngle)
        
        if self.atWaypoint(): # Watches to see if we pass the desired waypoint.
            self.startPos = robot.drivetrain.getPositions()
            self.passed = True
        
        if self.passed: # Have we gone through the waypoint?

            if self.notRanYet:  # Runs once at the waypoint.
                print(self.pointTracker)

                # try: # If it can't index them, then it's done. 
                #     self.desiredAngle = self.angles[self.pointTracker]
                #     self.desiredDistance = self.distances[self.pointTracker]

                # except(IndexError):
                #     print('f')
                #     self.pathFinished = True
                #     return
                
                # Below is the experimental.
                
                offsetDistance = (sum(robot.drivetrain.getPositions()) / 4) - (sum(self.startPos) / 4)
                
                nextDistance = self.distances[self.pointTracker]
                lastDistance = self.distances[self.pointTracker-1]
                
                nextAngle = self.angles[self.pointTracker]
                
                triangleHeight = nextDistance * math.cos(nextAngle * math.pi / 180)
                
                # Awful variable name I know, hard to explain.
                mainTriangleAngle = math.asin(triangleHeight / lastDistance) * 180 / math.pi
                
                finalTriangleAngle = 180 - ((90 - mainTriangleAngle) + nextAngle)
                
                distanceToSet=offsetDistance**2+nextDistance**2-2*offsetDistance*nextDistance*math.cos(finalTriangleAngle * math.pi / 180)
                angleToSet = math.asin((nextDistance * (math.sin(finalTriangleAngle * math.pi / 180))) / distanceToSet)
                
                self.notRanYet = False

                self.pointTracker += 1

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
                print('wheels aligned')
                
                robot.drivetrain.setPercents([0.51, 0.51, 0.5, 0.5]) # A little extra because the dt likes to turn.
                self.moveSet = True
                self.passed = False

        else:
            self.moveSet = False
            self.notRanYet = True
            
            

    def atWaypoint(self):
        count = 0
        print('\n')
        for position, start in zip(robot.drivetrain.getPositions(), self.startPos):
            print(abs(position - (start + self.desiredDistance)))
            if (
                abs(position - (start + self.desiredDistance)) < 2
            ):  # 2 inches is the tolerance.
                print('\n\nAt waypoint')
                return True
        
        return False

    def isFinished(self):
        return self.pathFinished

    def end(self, interrupted):
        robot.drivetrain.stop()
