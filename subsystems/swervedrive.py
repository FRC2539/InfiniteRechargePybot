from wpimath.kinematics import (
    SwerveDrive4Odometry,
    SwerveDrive4Kinematics,
    SwerveModuleState,
)
from wpimath.geometry import Translation2d, Rotation2d, Pose2d

from .cougarsystem import *
from .basedrive import BaseDrive
from .swervemodule import SwerveModule

import ports
import constants

import math


class SwerveDrive(BaseDrive):
    def __init__(self):
        super().__init__()

        """
        "Rollers? Where we're going, we don't need 'rollers'." - Ben Bistline, 2021
        
        The constructor for the class. When returning lists, it should follow like:
        [front left, front right, back left, back right]
        """

        if not constants.drivetrain.swerveStyle:
            self.move = self.tankMove
            self._calculateSpeeds = self.tankCalculateSpeeds

        self.isFieldOriented = True

        self.wheelBase = (
            constants.drivetrain.wheelBase
        )  # These are distances across the robot; horizontal, vertical, diagonal.
        self.trackWidth = constants.drivetrain.trackWidth
        self.r = math.sqrt(self.wheelBase ** 2 + self.trackWidth ** 2)

        self.speedLimit = (
            constants.drivetrain.speedLimit
        )  # Override the basedrive without editing the file.

        self.modules = [
            SwerveModule(  # Front left module.
                ports.drivetrain.frontLeftDriveID,
                ports.drivetrain.frontLeftTurnID,
                ports.drivetrain.frontLeftCANCoder,
                self.speedLimit,
                -255.761719,
            ),
            SwerveModule(  # Front right module.
                ports.drivetrain.frontRightDriveID,
                ports.drivetrain.frontRightTurnID,
                ports.drivetrain.frontRightCANCoder,
                self.speedLimit,
                -273.8672,
                invertedDrive=constants.drivetrain.swerveStyle,  # Invert for some reason?
            ),
            SwerveModule(  # Back left module.
                ports.drivetrain.backLeftDriveID,
                ports.drivetrain.backLeftTurnID,
                ports.drivetrain.backLeftCANCoder,
                self.speedLimit,
                -41.484375,
            ),
            SwerveModule(  # Back right module.
                ports.drivetrain.backRightDriveID,
                ports.drivetrain.backRightTurnID,
                ports.drivetrain.backRightCANCoder,
                self.speedLimit,
                -129.726563,
                invertedDrive=constants.drivetrain.swerveStyle,  # Invert for some reason. Ezra's going nuts lol.
            ),
        ]

        self.swerveKinematics = (
            SwerveDrive4Kinematics(  # X and Y components of center offsets.
                Translation2d(0.427799754, 0.427799754),  # Front left module
                Translation2d(0.427799754, -0.427799754),  # Front right module
                Translation2d(-0.427799754, 0.427799754),  # Back left module
                Translation2d(-0.427799754, -0.427799754),  # Back right module
            )
        )

        self.swerveOdometry = SwerveDrive4Odometry(
            self.swerveKinematics,
            self.navX.getRotation2d(),
            Pose2d(0, 0, Rotation2d(0)),
        )

        self.resetOdometry()
        self.resetGyro()
        self.PosX = 0
        self.PosY = 0
        self.LastPositions = self.getPositions()

    def periodic(self):
        """
        Loops whenever there is robot code. I recommend
        feeding networktable values here.
        """

        self.feed()  # Update the desired

        self.updateOdometry()

        Angles = self.getModuleAngles()
        Distance = []
        Positions = self.getPositions()
        for pos, lPos in zip(Positions, self.LastPositions):
            Distance.append(pos - lPos)
        VectorX = 0
        VectorY = 0
        for angle, distance in zip(Angles, Distance):
            VectorX += math.cos(math.radians(angle - 180)) * distance
            VectorY += math.sin(math.radians(angle - 180)) * distance
        VectorX = VectorX / 4
        VectorY = VectorY / 4
        self.PosX += VectorX
        self.PosY += VectorY

        self.LastPositions = self.getPositions()

    def GenerateRobotVector(self):
        Angles = self.getModuleAngles()
        Speeds = self.getSpeeds()
        VectorX = 0
        VectorY = 0
        for angle, speed in zip(Angles, Speeds):
            VectorX += math.cos(math.radians(angle - 180)) * speed
            VectorY += math.sin(math.radians(angle - 180)) * speed
        VectorX = VectorX / 4
        VectorY = VectorY / 4
        return VectorX, VectorY

    def updateOdometry(self):
        """
        Updates the WPILib odometry object
        using the gyro and the module states.
        """

        states = self.getModuleStates()

        self.swerveOdometry.update(
            self.navX.getRotation2d(),
            states[0],  # 0
            states[1],  # 1
            states[2],  # 2
            states[3],  # 3
        )

    def resetOdometry(self, pose=Pose2d(0, 0, Rotation2d(0))):
        """
        Resets the odometry to a given position, typically the one used when starting a trajectory.
        """
        self.swerveOdometry.resetPosition(pose, self.navX.getRotation2d())

    def getSwervePose(self):
        """
        Get the odometry's idea of the position
        """
        return self.swerveOdometry.getPose()

    def getChassisSpeeds(self):
        """
        Returns the robots velocity and heading, using
        module states, in the form of a ChassisSpeeds object.
        """

        return self.swerveKinematics.toChassisSpeeds(self.getModuleStates())

    def getChassisSpeedsData(self):
        """
        Basically the same thing as getChassisSpeeds, but this one
        extracts the data and returns the useful stuff in a list, which
        looks like this: [vx_fps, vy_fps, omega_dps].
        """

        speeds = self.swerveKinematics.toChassisSpeeds(self.getModuleStates())

        return [speeds.vy_fps, -speeds.vx_fps, speeds.omega_dps]

    def _configureMotors(self):
        """
        Configures the motors. Shouldn't need this.
        """

        self.activeMotors = self.motors[
            0:2
        ]  # Don't actually need these, this just keeps basedrive happy.

    def _calculateSpeeds(self, x, y, rotate):
        """
        Gonna take this nice and slow. Declaring variables to be simple,
        should try to walk through while coding.
        """

        """
        'self.getAngle()' is the robot's heading, 
        multiply it by pi over 180 to convert to radians.
        """

        theta = self.getAngleTo(0) * (
            math.pi / 180
        )  # Gets the offset to zero, -180 to 180.

        if (
            self.isFieldOriented
        ):  # Are we field-centric, as opposed to robot-centric. A tank drive is robot-centric, for example.

            temp = y * math.cos(theta) + x * math.sin(
                theta
            )  # just the new y value being temporarily stored.
            x = -y * math.sin(theta) + x * math.cos(theta)
            y = temp

        """
        The bottom part is the most confusing part, but it basically uses ratios and vectors with the
        pythagorean theorem to calculate the velocities.
        """
        A = x - rotate * (self.wheelBase / self.r)  # Use variables to simplify it.
        B = x + rotate * (self.wheelBase / self.r)
        C = y - rotate * (self.trackWidth / self.r)
        D = y + rotate * (self.trackWidth / self.r)

        ws1 = math.sqrt(B ** 2 + D ** 2)  # Front left speed
        ws2 = math.sqrt(B ** 2 + C ** 2)  # Front right speed
        ws3 = math.sqrt(A ** 2 + D ** 2)  # Back left speed
        ws4 = math.sqrt(A ** 2 + C ** 2)  # Back right speed

        wa1 = math.atan2(B, D) * 180 / math.pi  # Front left angle
        wa2 = math.atan2(B, C) * 180 / math.pi  # Front right angle
        wa3 = math.atan2(A, D) * 180 / math.pi  # Back left angle
        wa4 = math.atan2(A, C) * 180 / math.pi  # Back right angle

        speeds = [ws2, ws1, ws4, ws3]  # It is in order (FL, FR, BL, BR).
        angles = [wa2, wa1, wa4, wa3]  # It is in order (FL, FR, BL, BR).

        newSpeeds = speeds  # Do NOT delete! This IS used!
        newAngles = angles

        maxSpeed = max(speeds)  # Find the largest speed.
        minSpeed = min(speeds)  # Find the smallest speed.

        if (
            maxSpeed > 1
        ):  # Normalize speeds if greater than 1, but keep then consistent with each other.
            speeds[:] = [
                speed / maxSpeed for speed in speeds
            ]  # We can do this by dividing ALL by the largest value.

        if (
            minSpeed < -1
        ):  # Normalize speeds if less than -1, but keep then consitent with each other.
            speeds[:] = [
                speed / minSpeed * -1 for speed in speeds
            ]  # We can do this by dividing ALL by the smallest value. The negative maintains the signs.

        magnitude = math.sqrt(
            (x ** 2) + (y ** 2)
        )  # Pythagorean theorem, vector of joystick.
        if magnitude > 1:
            magnitude = 1

        speeds[:] = [
            speed * magnitude for speed in speeds
        ]  # Ensures that the speeds of the motors are relevant to the joystick input.
        return newSpeeds, angles  # Return the calculated speed and angles.

    def move(self, x, y, rotate):
        """
        Turns coordinate arguments into motor outputs.
        Short-circuits the rather expensive movement calculations if the
        coordinates have not changed.
        """
        if [x, y, rotate] == [0, 0, 0]:
            self.stop()
            return

        """Prevent drift caused by small input values"""
        x = math.copysign(max(abs(x) - self.deadband, 0), x)
        y = math.copysign(max(abs(y) - self.deadband, 0), y)
        rotate = math.copysign(max(abs(rotate) - (self.deadband + 0.05), 0), rotate)

        speeds, angles = self._calculateSpeeds(x, y, rotate)

        if (
            x == 0 and y == 0 and rotate != 0
        ):  # The robot won't apply power if it's just rotate (fsr?!)
            for module, angle in zip(
                self.modules, angles
            ):  # You're going to need encoders, so only focus here.
                module.setWheelAngle(angle)
                module.setWheelSpeed(abs(rotate))

        else:
            for module, speed, angle in zip(
                self.modules, speeds, angles
            ):  # You're going to need encoders, so only focus here.
                module.setWheelAngle(angle)
                module.setWheelSpeed(abs(math.sqrt(speed ** 2 + rotate ** 2)))

    def tankMove(self, y, rotate):
        if [y, rotate] == self.lastInputs:
            return

        self.lastInputs = [y, rotate]

        """Prevent drift caused by small input values"""
        if self.useEncoders:
            y = math.copysign(max(abs(y) - self.deadband, 0), y)
            rotate = math.copysign(max(abs(rotate) - self.deadband, 0), rotate)

        speeds = self.tankCalculateSpeeds(y, rotate)

        print("s " + str(speeds))

        for module, speed in zip(self.modules, speeds):
            module.setWheelAngle(0)
            module.setWheelSpeed(speed)

    def tankCalculateSpeeds(self, y, rotate):
        return [y + rotate, -y + rotate, y + rotate, -y + rotate]  # FL, FR, BL, BR

    def stop(self):
        """
        Stops the modules.
        """
        for module in self.modules:
            module.stopModule()

    def longStop(self):
        """
        Returns true when all wheel speeds
        are zero.
        """
        self.stop()
        while self.getSpeeds().count(0) < 3:
            pass

    def resetEncoders(self, anArgumentAsWell=0):
        """
        Resets all drive encoders to 0 by default.
        """
        for module in self.modules:
            module.resetDriveEncoders(anArgumentAsWell)

    def setProfile(self, profile):
        """
        Sets the profile for both drive and turn motors.
        """
        for module in self.modules:
            module.setModuleProfile(profile)

    def setModuleProfiles(self, id_=0, drive=True, turn=True):
        """
        Sets the PID profiles for each of the modules.
        This one accepts an optional turn and drive.
        """
        for module in self.modules:
            module.setModuleProfile(id_, drive, turn)

    def updateCANCoders(self, positions: list):
        """
        Sets the position of the CANCoders. Be careful using
        this method!
        """
        for module, position in zip(self.modules, positions):
            module.updateCANCoder(position)

    def setSpeedLimit(self, speed):
        """
        Sets the speed limit of the drive motor in
        inches per second.
        """
        self.speedLimit = speed

        for module in self.modules:
            module.speedLimit = speed

    def setFieldOriented(self, fieldCentric=True):
        """
        Changes the orientation of the robot. It should almost always be
        field centric on a swerve robot.
        """
        self.isFieldOriented = fieldCentric

    def getModuleStates(self):
        """
        Returns a list of SwerveModuleState objects.
        Usefulf for chassis speeds and odometry.
        """

        states = []
        for module in self.modules:
            s = module.getWheelSpeed() / 39.3701  # In Meters Per Second
            a = Rotation2d(math.radians(module.getWheelAngle() - 180))
            states.append(SwerveModuleState(s, a))

        return states

    def setModuleStates(self, moduleStates):
        """
        Set the states of the modules. Used by trajectory stuff.
        """
        for module, state in zip(self.modules, moduleStates):
            module.setState(state)

    def getSpeeds(self, inIPS=True):  # Defaults to giving in inches per second.
        """
        Returns the speeds of the wheel.
        """
        return [module.getWheelSpeed(inIPS) for module in self.modules]

    def setSpeeds(self, speeds: list):  # Set a speed in inches per second.
        """
        Sets the speeds of the wheels in inches per second.
        It takes a list. Please use setUniformModuleSpeed if
        you want to set the same speed amongst all the modules.
        """
        for module, speed in zip(self.modules, speeds):
            module.setWheelSpeed(speed)

    def setUniformModuleSpeed(self, speed: float):  # Set a speed in inches per second.
        """
        Sets a uniform speed to eall the drive motors in inches per
        second. This takes a float because all modules use
        the same speed. Use the setSpeeds method if you want to pass
        a list of different speeds.
        """
        for module in self.modules:
            module.setWheelSpeed(speed)

    def getPercents(self):
        """
        Returns the percent outputs of each drive motor.
        """
        return [module.getWheelPercent() for module in self.modules]

    def setPercents(self, speeds: list):
        """
        Sets the percent speed of each module's drive motor.
        """
        for module, speed in zip(self.modules, speeds):
            module.setWheelPercent(speed)

    def setUniformModulePercent(self, speed: float):
        """
        Sets a uniform percent to the drive motor
        of each module.
        """
        for module in self.modules:
            module.setWheelPercent(speed)

    def getModuleAngles(self):
        """
        Returns the CANCoder's absolute reading.
        Note, this does take into account the magnet
        offset which we set at the beginning.
        I think, 180 is forward, 0 is backwards. It
        returns between 0 and 360.
        """

        # Add module in front, not to be confused with gyro! Returns degrees.
        return [module.getWheelAngle() % 360 for module in self.modules]

    def setModuleAngles(self, angles: list):  # Set a list of different angles.
        """
        Set the angle of the wheel using the turn motor.
        This method takes a list of angles, 0-360 degrees.
        """

        for module, angle in zip(self.modules, angles):
            module.setWheelAngle(angle)

    def setUniformModuleAngle(self, angle: int):
        """
        Set the angle of the wheel using the turn motor.
        This method takes a universal angle to set to all
        modules. The angle should be 0-360 degrees.
        """
        for module in self.modules:
            module.setWheelAngle(angle)

    def getPositions(self, inInches=True):  # Defaults to giving in inches.
        """
        Returns the module position in inches (by default).
        """
        return [module.getModulePosition(inInches) for module in self.modules]

    def setPositions(self, positions: list):
        """
        Sets the position of the modules. It will go forward this many inches.
        I recommend using the setUniformModulePosition however.
        Remember, provide these in inches. It will go forward/back x many inches.
        """
        for module, position in zip(self.modules, positions):
            module.setModulePosition(position)

    def setUniformModulePosition(self, distance):
        """
        Sets a uniform distance for the drive motor to travel. Note,
        you should give the distance in inches. The modules will move this
        much in the direction they are facing.
        """
        for module in self.modules:
            module.setModulePosition(distance)

    # Cougar Course Below.

    def injectBetweenTwoPoints(self, startPoint: list, endPoint: list, spacing=1):
        """
        Used in CougarCourse. Adds additional points.
        """

        reverseNessesary = False
        print(startPoint)
        print("e " + str(endPoint))

        if startPoint[1] < endPoint[1]:
            x1, y1 = startPoint[0], startPoint[1]
            x2, y2 = endPoint[0], endPoint[1]
        elif startPoint[1] > endPoint[1]:
            x2, y2 = startPoint[0], startPoint[1]
            x1, y1 = endPoint[0], endPoint[1]
            reverseNessesary = True
        else:
            raise Exception("Start and end point cannot be the same!")

        pointsInBetween = [[x1, y1]]

        totalDistance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

        # Calculate spacing.
        numOfPoints = math.ceil(totalDistance / spacing)
        spacing = totalDistance / numOfPoints

        # Angle diff.
        theta = math.atan((y2 - y1) / (x2 - x1))

        for segment in range(numOfPoints):
            newX = math.sin(theta) * spacing + x1
            newY = math.cos(theta) * spacing + y1

            pointsInBetween.append([newX, newY])

            x1 = newX  # Override for next loop.
            y1 = newY  # Override for next loop.

        if reverseNessesary:
            pointsInBetween.reverse()

        return pointsInBetween

    def injectPoints(self, points: list, spacing=1):
        """
        Inject points between a series of points. Used in the CougarCourse.
        """
        final = []
        for point in points:
            startPoint = [point[0], point[1]]
            endPoint = [point[2], point[3]]

            pointsToInsert = self.injectBetweenTwoPoints(startPoint, endPoint, spacing)

            for point in pointsToInsert:
                final.append(point)

        return final

    def smoothPoints(
        self, path: list, weightData=0.75, weightSmooth=0.25, tolerance=0.001
    ):
        """
        Curves a lot of points. Used in
        CougarCourse.
        """
        newPath = path.copy()

        change = tolerance
        while change >= tolerance:  # You touch this, you die.
            change = 0
            i = 1
            while i < len(path) - 1:

                j = 0
                while j < len(path[i]):
                    aux = newPath[i][j]
                    newPath[i][j] += weightData * (
                        path[i][j] - newPath[i][j]
                    ) + weightSmooth * (
                        newPath[i - 1][j] + newPath[i + 1][j] - (2 * newPath[i][j])
                    )
                    change += abs(aux - newPath[i][j])

                    j += 1

                i += 1

        return newPath

    def assertDistanceAlongCurve(self, points: list):
        """
        Adds the distance travelled to the points by using
        the distance formula. Used in CougarCourse.
        """
        points[0].append(0)
        i = 1
        while i < len(points):
            points[i].append(
                points[i - 1][2]
                + math.sqrt(
                    (points[i][0] - points[i - 1][0]) ** 2
                    + (points[i][1] - points[i - 1][1]) ** 2
                )
            )
            i += 1

        return points

    def setCruiseVelocity(self, slow=False):
        """
        Changes the motion magic's max cruise velocity.
        Used in CougarCourse.
        """
        for module in self.modules:
            module.setDriveCruiseVelocity(slow)
