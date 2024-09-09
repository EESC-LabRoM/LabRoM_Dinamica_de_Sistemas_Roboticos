import numpy as np
from roboticstoolbox import DHRobot, RevoluteDH
import matplotlib.pyplot as plt
from time import sleep

# Define the Puma 560 robot using DH parametersf

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

    # Function to interpolate between two sets of joint angles
    def interpolate_motion(start_angles, end_angles, steps=20, delay=0.02):
        for i in range(steps + 1):
            # Interpolate joint angles
            joint_angles = start_angles + (end_angles - start_angles) * (i / steps)
            # Plot the robot's current configuration
            robot.plot(joint_angles, block=False)
            plt.pause(0.001)  # Update plot
            sleep(delay)      # Slow down the animation

    # Simulation for forward kinematics
    def simulate_forward_kinematics():
        print("\n--- Forward Kinematics Simulation ---")
        try:
            start_angles = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])  # Start with the default position
            while True:
                joint_angles = np.array(list(map(float, input("Enter 6 joint angles in radians separated by spaces: ").split())))
                if len(joint_angles) != 6:
                    raise ValueError("Please input exactly 6 angles.")

                # Perform forward kinematics
                T = robot.fkine(joint_angles)
                print("Forward kinematics (end-effector pose):\n", T)

                # Interpolate between the current and target joint angles for smooth motion
                interpolate_motion(start_angles, joint_angles)

                # Update the starting angles for the next motion
                start_angles = joint_angles
        except ValueError as e:
            print(e)

    # Simulation for inverse kinematics
    def simulate_inverse_kinematics():
        print("\n--- Inverse Kinematics Simulation ---")
        try:
            start_angles = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])  # Start with the default position
            while True:
                position = np.array(list(map(float, input("Enter the x, y, z position (in meters) separated by spaces: ").split())))
                if len(position) != 3:
                    raise ValueError("Please input exactly 3 values for x, y, z.")

                # Target pose with identity rotation matrix and the input position
                T_target = np.eye(4)
                T_target[0:3, 3] = position

                # Perform inverse kinematics using the Levenberg-Marquardt method
                solution = robot.ikine_LM(T_target)
                if solution.success:
                    print(f"Inverse kinematics (joint angles): {solution.q}")

                    # Interpolate between the current and target joint angles for smooth motion
                    interpolate_motion(start_angles, solution.q)

                    # Update the starting angles for the next motion
                    start_angles = solution.q
                else:
                    print("Inverse kinematics failed to find a valid solution.")
        except ValueError as e:
            print(e)

    # Choose simulation type
    while True:
        choice = input("Choose simulation type: (f)orward kinematics, (i)nverse kinematics, (q)uit: ").lower()
        if choice == 'f':
            simulate_forward_kinematics()
        elif choice == 'i':
            simulate_inverse_kinematics()
        elif choice == 'q':
            break
        else:
            print("Invalid choice. Please select 'f', 'i', or 'q'.")

if __name__ == "__main__":
    puma560()

'''
0.3 0.5 0.7 0.9 0.2 0.4
1.0 -0.8 0.7 -1.2 0.3 1.1
-1.5 1.2 -1.0 0.8 -0.5 1.4

0.3 -0.2 0.5
0.2 0.3 0.8
-0.4 -0.6 0.5

'''
