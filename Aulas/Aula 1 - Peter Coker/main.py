import numpy as np
from roboticstoolbox import DHRobot, RevoluteDH, PrismaticDH
import matplotlib.pyplot as plt
from time import sleep


# Define a simple robot with a prismatic joint using DH parameters
def stanford_arm():
    # DH parameters with at least one prismatic joint
    robot = DHRobot([
        RevoluteDH(d=0, a=0, alpha=-np.pi/2),                  # Joint 1
        PrismaticDH(theta=0, a=0, alpha=np.pi/2, qlim=[0,1]),  # Prismatic Joint 2
        RevoluteDH(d=0, a=0, alpha=0)                          # Joint 3
    ], name='Stanford Arm')

    # Print robot model
    print(robot)

    # Define joint configuration (radians for revolute, meters for prismatic)
    joint_config = [np.pi/4, 0.2, np.pi/6]  # Joint 2 is prismatic with d = 0.2 meters

    # Perform forward kinematics
    T = robot.fkine(joint_config)
    print("Forward kinematics (end-effector pose):\n", T)

    # Perform inverse kinematics using the Levenberg-Marquardt method
    solution = robot.ikine_LM(T)
    print("Inverse kinematics (joint configuration):\n", solution.q)

    # Plot the robot in its current configuration
    robot.plot(joint_config)
    plt.show()

    # Use the inverse kinematics solution as initial joint configuration for the teach mode
    initial_joint_config = solution.q

    # Interactive teach mode with initial joint configuration
    robot.teach(initial_joint_config)

# Define the Puma 560 robot using DH parameters
def puma560():
    # Standard DH parameters for the Puma 560
    robot = DHRobot([
        RevoluteDH(d=0.6718,  a=0,       alpha=np.pi/2),  # Joint 1
        RevoluteDH(d=0,       a=0.4318,  alpha=0),        # Joint 2
        RevoluteDH(d=0.15005, a=0.0203,  alpha=-np.pi/2), # Joint 3
        RevoluteDH(d=0.4318,  a=0,       alpha=np.pi/2),  # Joint 4
        RevoluteDH(d=0,       a=0,       alpha=-np.pi/2), # Joint 5
        RevoluteDH(d=0,       a=0,       alpha=0)         # Joint 6
    ], name='Puma 560')       

    # Print robot model
    print(robot)

    # Define joint angles (radians)
    joint_angles = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]

    # Perform forward kinematics
    T = robot.fkine(joint_angles)
    print("Forward kinematics (end-effector pose):\n", T)

    # Perform inverse kinematics using the Levenberg-Marquardt method
    solution = robot.ikine_LM(T)
    print("Inverse kinematics (joint angles):\n", solution.q)

    # Plot the robot in its current configuration
    robot.plot(joint_angles)
    plt.show()

    # Use the inverse kinematics solution as initial joint configuration for the teach mode
    initial_joint_angles = solution.q

    # Interactive teach mode with initial joint angles
    robot.teach(initial_joint_angles)

if __name__ == "__main__":
    puma560()
    #stanford_arm()