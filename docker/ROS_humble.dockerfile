# Use an official ROS Humble full desktop image as the base
FROM osrf/ros:humble-desktop-full

# Avoid prompts from APT during build by specifying non-interactive as the frontend
ARG DEBIAN_FRONTEND=noninteractive
# Set the timezone environment variable
ENV TZ=America/Sao_Paulo

# Define user-related arguments to create a non-root user inside the container
ARG USERNAME=ros2_ws
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create a new group and user with the specified UID and GID, create a config directory, and set ownership
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && mkdir /home/$USERNAME/.config && chown $USER_UID:$USER_GID /home/$USERNAME/.config

# Ensure runtime directory is created and accessible
RUN mkdir -p /tmp/runtime-ros2_ws && chown $USER_UID:$USER_GID /tmp/runtime-ros2_ws

# Add environment variable setting
ENV XDG_RUNTIME_DIR=/tmp/runtime-ros2_ws

# Update the package list, install sudo, configure sudoers for the new user without password prompts, and clean up APT lists
RUN apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 -R /etc/sudoers.d/$USERNAME \
    && rm -rf /var/lib/apt/lists/*

# Update package list and install git
RUN apt-get update \
    && apt-get install -y git-all ripgrep

# Update package list and install various packages for development with ROS, including visualization tools, development libraries, and Python packages
RUN apt-get update && apt-get install -y \
    # URDF
    ros-humble-robot-state-publisher \
    ros-humble-joint-state-publisher \
    ros-humble-joint-state-publisher-gui \
    ros-humble-xacro \
    # # ROS core and utilities
    # python3-rosdep \
    # python3-rosinstall \
    # python3-rosinstall-generator \
    # python3-wstool \
    # python3-catkin-tools \
    # python3-colcon-common-extensions \
    # ros-noetic-rqt \
    # ros-noetic-rqt-common-plugins \
    # ros-noetic-ros-tutorials \
    # ros-noetic-rviz \
    # ros-noetic-teleop-twist-keyboard \
    # ros-noetic-rqt-multiplot \
    # # Development tools
    # wget \
    # git \
    # build-essential \
    # ffmpeg \
    # # Python packages
    # python3 \
    # python3-pip \
    # python3-numpy \
    # python3-opencv \
    # # ROS basic simulation and visualization packages
    # ros-noetic-gazebo-ros-pkgs \
    # ros-noetic-hector-gazebo-plugins \
    # # Sensor and control packages
    # ros-noetic-usb-cam \
    # ros-noetic-perception \
    # ros-noetic-cv-bridge \
    # ros-noetic-pointcloud-to-laserscan \
    # ros-noetic-velodyne-description \
    # ros-noetic-velodyne-gazebo-plugins \
    # ros-noetic-interactive-markers \
    # ros-noetic-diff-drive-controller \
    # ros-noetic-joint-state-controller \
    # ros-noetic-joint-trajectory-controller \
    # ros-noetic-joy \
    # ros-noetic-controller-manager \
    # ros-noetic-teleop-twist-joy \
    # ros-noetic-twist-mux \
    # # Core ROS packages
    # ros-noetic-roscpp \
    # ros-noetic-sensor-msgs \
    # ros-noetic-roslint \
    # ros-noetic-robot-localization \
    # ros-noetic-turtlesim \
    # ros-noetic-tf2-tools \
    # # Libraries for robotic applications
    # liburdfdom-dev \
    # liboctomap-dev \
    # libassimp-dev \
    # libboost-all-dev \
    # libeigen3-dev \
    # mesa-utils \
    # libgl1-mesa-dri \
    # libgl1-mesa-glx \
    # x11-apps \
    # intel-media-va-driver-non-free \
    # libdrm-intel1 \
    # ros-noetic-urdf \
    # Clean up APT when done.
    && rm -rf /var/lib/apt/lists/*

# Assuming your ROS workspace in the container is located at /home/ros_ws

# Copy custom entrypoint script and .bashrc configuration from the host to the container
COPY config/entrypoint.sh /entrypoint.sh
COPY config/bashrc /home/${USERNAME}/.bashrc

# Set the custom script to be the container's entrypoint, this script is executed when the container starts
ENTRYPOINT [ "/bin/bash", "/entrypoint.sh" ]

# Default command when the container is run, if no other commands are specified
CMD [ "bash" ]
