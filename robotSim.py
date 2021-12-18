#Robot Simulation primary file (do not expect this to work, still fiddling around with stuff).

#import wpimath.VecBuilder (did not see in docs).
import wpimath.controller #.PIDController? (Did not see in docs).
import wpimath.system.plant.DCMotor

from wpilib import Encoder
from wpilib import Joystick
from wpilib import RobotController
from wpilib import TimedRobot
from wpilib import PWMSparkMax

#wpilib.smartdashboard for python?
#Use python standard library for utilities.

from wpilib.simulation import RoboRioSim

#All import from LinearSystemSim_X_X_X
from wpilib.simulation import FlyWheelSim
from wpilib.simulation import DifferentialDrivetrainSim
from wpilib.simulation import ElevatorSim
from wpilib.simulation import SingleJointedArmSim
from wpilib.simulation import BatterySim

#ElevatorSim


