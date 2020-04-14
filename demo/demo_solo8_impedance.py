##################################################################################################################
## Demo file showing how to import and use the leg impedance control for solo 8 DOF
#################################################################################################################
## Author: Julian Viereck
## Date: 20/09/2019
#################################################################################################################

import numpy as np

import time

import os
import rospkg
import pybullet as p
import pinocchio as se3
from pinocchio.utils import se3ToXYZQUAT

from robot_properties_solo.config import Solo8Config
from robot_properties_solo.solo8wrapper import Solo8Robot

from py_blmc_controllers.solo_impedance_controller import Solo8ImpedanceController

from pinocchio.utils import zero
from matplotlib import pyplot as plt


# Create a robot instance. This initializes the simulator as well.
robot = Solo8Robot()
tau = np.zeros(8)

# Reset the robot to some initial state.
q0 = np.matrix(Solo8Config.initial_configuration).T
dq0 = np.matrix(Solo8Config.initial_velocity).T
robot.reset_state(q0, dq0)

###################### impedance controller demo #################################

x_des = 4*[0.0, 0.0, -0.25]
xd_des = 4*[0,0,0]
kp = 4 * [200,200,200]
kd = 4 * [10.0,10.0,10.0]
f = np.zeros(18)
f = 4*[0.0, 0.0, (2.2*9.8)/4]
##################################################################################

solo_leg_ctrl = Solo8ImpedanceController(robot)

# Run the simulator for 100 steps
for i in range(4000):
    # TODO: Implement a controller here.
    # Step the simulator.
    p.stepSimulation()
    time.sleep(0.001) # You can sleep here if you want to slow down the replay
    # Read the final state and forces after the stepping.
    q, dq = robot.get_state()
    tau = solo_leg_ctrl.return_joint_torques(q,dq,kp,kd,x_des,xd_des,f)
    robot.send_joint_command(tau)
