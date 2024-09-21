# Usa uma imagem oficial completa do ROS Humble Desktop como base
FROM osrf/ros:humble-desktop-full

# Evita prompts do APT durante a construção, especificando non-interactive como frontend
ARG DEBIAN_FRONTEND=noninteractive
# Define a variável de ambiente para o fuso horário
ENV TZ=America/Sao_Paulo

# Set the location of the Gazebo Plugin Path
ENV GAZEBO_PLUGIN_PATH=/usr/lib/x86_64-linux-gnu/gazebo-11/plugins:$GAZEBO_PLUGIN_PATH

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
RUN mkdir -p /tmp/runtime-ros2_ws && chown $USER_UID:$USER_GID /tmp/runtime-ros2_ws

# Adiciona a variável de ambiente para definir o diretório de runtime
ENV XDG_RUNTIME_DIR=/tmp/runtime-ros2_ws

# # Atualiza a lista de pacotes e instala git e ripgrep
# RUN apt-get update \
#     && apt-get install -y git-all ripgrep

# Atualiza a lista de pacotes e instala várias ferramentas de desenvolvimento para ROS, incluindo ferramentas de visualização e bibliotecas de desenvolvimento
RUN apt-get update && apt-get install -y \
    git-all ripgrep \
    # URDF (Universal Robot Description Format)
    ros-humble-robot-state-publisher \
    ros-humble-joint-state-publisher \
    ros-humble-joint-state-publisher-gui \
    ros-humble-xacro \
    ros-humble-rviz2 \
    && rm -rf /var/lib/apt/lists/*

# Cria o diretório para o workspace ROS e ajusta a propriedade
RUN mkdir -p /home/$USERNAME/ && chown $USER_UID:$USER_GID /home/$USERNAME/

# Copia o script de entrypoint personalizado e o arquivo .bashrc do host para o contêiner
COPY config/entrypoint.sh /entrypoint.sh
COPY config/bashrc /home/${USERNAME}/.bashrc

# Define o script personalizado como o entrypoint do contêiner, que será executado quando o contêiner iniciar
ENTRYPOINT [ "/bin/bash", "/entrypoint.sh" ]

# Comando padrão a ser executado quando o contêiner for iniciado, caso nenhum outro comando seja especificado
CMD [ "bash" ]
