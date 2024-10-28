# Usa uma imagem oficial completa do ROS Humble Desktop como base
FROM osrf/ros:humble-desktop-full

# Evita prompts do APT durante a construção, especificando non-interactive como frontend
ARG DEBIAN_FRONTEND=noninteractive
# Define a variável de ambiente para o fuso horário
ENV TZ=America/Sao_Paulo

# Define argumentos relacionados ao usuário para criar um usuário não-root dentro do contêiner
ARG USERNAME=ros2_ws
ARG USER_UID=1000
ARG USER_GID=$USER_UID


# Crie um novo grupo e usuário, configure diretórios e instale o sudo
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && mkdir /home/$USERNAME/.config && chown $USER_UID:$USER_GID /home/$USERNAME/.config \
    && apt-get update \
    && apt-get install -y sudo \
    && echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && rm -rf /var/lib/apt/lists/*

# Garante que o diretório runtime seja criado e acessível
RUN mkdir -p /tmp/runtime-ros2_ws \
    && chown $USER_UID:$USER_GID /tmp/runtime-ros2_ws \
    && chmod 0700 /tmp/runtime-ros2_ws

# Adiciona a variável de ambiente para definir o diretório de runtime
ENV XDG_RUNTIME_DIR=/tmp/runtime-ros2_ws

# Instalação de dependências básicas e ferramentas de desenvolvimento
RUN apt-get update && apt-get install -y \
    git-all ripgrep \
    libserial-dev \
    python3-pip \
    && pip install pyserial flask flask-ask-sdk ask-sdk \
    && rm -rf /var/lib/apt/lists/*

# Instalação de ferramentas ROS para URDF e visualização
RUN apt-get update && apt-get install -y \
    ros-humble-robot-state-publisher \
    ros-humble-joint-state-publisher \
    ros-humble-joint-state-publisher-gui \
    ros-humble-xacro \
    ros-humble-rviz2 \
    && rm -rf /var/lib/apt/lists/*

# Instalação de pacotes MoveIt 2
RUN apt-get update && apt-get install -y \
    ros-humble-moveit \
    ros-humble-moveit-setup-assistant \
    ros-humble-moveit-ros-planning \
    ros-humble-moveit-core \
    ros-humble-moveit-ros-control-interface \
    ros-humble-moveit-kinematics \
    ros-humble-moveit-planners-ompl \
    ros-humble-moveit-simple-controller-manager \
    && rm -rf /var/lib/apt/lists/*

# Instalação de pacotes de controle ROS 2 (ros2_control)
RUN apt-get update && apt-get install -y \
    ros-humble-controller-manager \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-joint-state-broadcaster \
    ros-humble-joint-trajectory-controller \
    && rm -rf /var/lib/apt/lists/*

# Instalação de pacotes Gazebo e integração com ROS 2
RUN apt-get update && apt-get install -y \
    ros-humble-ros-ign \
    ros-humble-ign-ros2-control \
    ros-humble-ros-ign-bridge \
    ros-humble-ros-ign-gazebo \
    ros-humble-ros-ign-gazebo-demos \
    && rm -rf /var/lib/apt/lists/*

# Cria o diretório para o workspace ROS e ajusta a propriedade
RUN mkdir -p /home/$USERNAME/ros2_ws && chown $USER_UID:$USER_GID /home/$USERNAME/ros2_ws
RUN usermod -aG video ros2_ws
# Copia o script de entrypoint personalizado e o arquivo .bashrc do host para o contêiner
COPY config/entrypoint.sh /entrypoint.sh
COPY config/bashrc /home/${USERNAME}/.bashrc

# Define o script personalizado como o entrypoint do contêiner, que será executado quando o contêiner iniciar
ENTRYPOINT [ "/bin/bash", "/entrypoint.sh" ]

# Comando padrão a ser executado quando o contêiner for iniciado, caso nenhum outro comando seja especificado
CMD [ "bash" ]
