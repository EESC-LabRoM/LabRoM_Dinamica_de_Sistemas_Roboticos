#!/bin/bash
# Specifies that the script should be executed using the Bash shell.

# Check if the current directory path ends with 'LabRoM_Dinamica_de_Sistemas_Roboticos'.
if [[ $PWD = */LabRoM_Dinamica_de_Sistemas_Roboticos ]]; then

    # Automatically detects an NVIDIA GPU and attempts to utilize it.
    if [ -z "$(lspci | grep NVIDIA)" ]; then
        USE_GPUS=""
        # If no NVIDIA GPU is detected, set USE_GPUS to an empty string.
        echo "NVIDIA's GPU Não foi detectada."
        # Prints message indicating no NVIDIA GPU was detected.
    else
        USE_GPUS="--gpus all"
        # If an NVIDIA GPU is detected, enable GPU support for the Docker container.
        echo "NVIDIA's GPU foi detectada. Ativando '--gpus all' flag."
        # Prints message indicating NVIDIA GPU was detected and the GPU flag is activated.
    fi

    # Allow local connections to X server
    xhost +local:docker

    # Run the Docker container with GPU support if available
    docker run -it --rm \
        $USE_GPUS \
        --name ros_humble \
        --user ros2_ws \
        -e QT_X11_NO_MITSHM=1 \
        -e XDG_RUNTIME_DIR=/tmp/runtime-ros2_ws \
        -e DISPLAY=$DISPLAY \
        -e LIBGL_ALWAYS_SOFTWARE=1 \
        --network=host \
        --ipc=host \
        --privileged \
        --device /dev/video0 \
        -v /dev/video0:/dev/video0 \
        -v /dev/dri:/dev/dri \
        -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
        -v "$PWD/ros2_ws:/home/ros2_ws/ros2_ws" \
        --workdir /home/ros2_ws/ros2_ws \
        ros2_ws:humble

elif [[ ! $PWD = */LabRoM_Dinamica_de_Sistemas_Roboticos ]]; then
    # Checks if the current directory is not 'LabRoM_Dinamica_de_Sistemas_Roboticos'.
    echo -e "You must be in the 'LabRoM_Dinamica_de_Sistemas_Roboticos' directory to run this command."
    # Informs the user that they must be in the correct directory to run the script.
    echo -e "Você deve estar na pasta 'LabRoM_Dinamica_de_Sistemas_Roboticos' para rodar esse comando."
    # Informs the user in Portuguese of the same requirement.
    exit 1
    # Exits the script with a status of 1, indicating an error.
fi
