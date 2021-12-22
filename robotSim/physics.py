#Robot Simulation physics test file.

import wpilib.simulation

from pyfrc.physics.core import PhysicsInterface
from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units

#import wpimath.VecBuilder (did not see in docs).
#import wpimath.controller #.PIDController? (Did not see in docs).
#import wpimath.system.plant.DCMotor

#from wpilib import Encoder
#from wpilib import Joystick
#from wpilib import RobotController
#from wpilib import TimedRobot
#from wpilib import PWMSparkMax

##wpilib.smartdashboard for python?
##Use python standard library for utilities.

#from wpilib.simulation import RoboRioSim

##All import from LinearSystemSim_X_X_X
#from wpilib.simulation import FlyWheelSim
#from wpilib.simulation import DifferentialDrivetrainSim
#from wpilib.simulation import ElevatorSim
#from wpilib.simulation import SingleJointedArmSim
#from wpilib.simulation import BatterySim

#ElevatorSim

class PhysicsEngine:
    """
    Example: Simulates a motor moving something that strikes two limit switches,
    one on each end of the track. Obviously, this is not particularly
    realistic, but it's good enough to illustrate the point
    """

    def __init__(self, physics_controller):

        self.physics_controller = physics_controller

                # Motors
                self.l_motor = wpilib.simulation.PWMSim(1)
                self.r_motor = wpilib.simulation.PWMSim(2)

                self.dio1 = wpilib.simulation.DIOSim(1)
                self.dio2 = wpilib.simulation.DIOSim(2)
                self.ain2 = wpilib.simulation.AnalogInputSim(2)

                self.motor = wpilib.simulation.PWMSim(4)

                # Gyro
                self.gyro = wpilib.simulation.AnalogGyroSim(1)

                self.position = 0

                # Change these parameters to fit your robot!
                bumper_width = 3.25 * units.inch

                # fmt: off
                self.drivetrain = tankmodel.TankModel.theory(
                    motor_cfgs.MOTOR_CFG_CIM,           # motor configuration
                    110 * units.lbs,                    # robot mass
                    10.71,                              # drivetrain gear ratio
                    2,                                  # motors per side
                    22 * units.inch,                    # robot wheelbase
                    23 * units.inch + bumper_width * 2, # robot width
                    32 * units.inch + bumper_width * 2, # robot length
                    6 * units.inch,                     # wheel diameter
                )
                # fmt: on

    def update_sim(self, now: float, tm_diff: float) -> None:
            """
            Called when the simulation parameters for the program need to be
            updated.
            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
                            
            All physics simulators go here (I think).
            """

            # Simulate the drivetrain
            l_motor = self.l_motor.getSpeed()
            r_motor = self.r_motor.getSpeed()

            transform = self.drivetrain.calculate(l_motor, r_motor, tm_diff)
            pose = self.physics_controller.move_robot(transform)

            # Update the gyro simulation
            # -> FRC gyros are positive clockwise, but the returned pose is positive
            #    counter-clockwise
            self.gyro.setAngle(-pose.rotation().degrees())

            # update position (use tm_diff so the rate is constant)
            self.position += self.motor.getSpeed() * tm_diff * 3

            # update limit switches based on position
            if self.position <= 0:
                switch1 = True
                switch2 = False

            elif self.position > 10:
                switch1 = False
                switch2 = True

            else:
                switch1 = False
                switch2 = False

            # set values here
            self.dio1.setValue(switch1)
            self.dio2.setValue(switch2)
            self.ain2.setVoltage(self.position)


