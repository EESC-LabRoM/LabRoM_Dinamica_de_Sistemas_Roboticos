from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
  
  """ 
    Função para gerar a descrição do lançamento.
    
    Esta função define a descrição do lançamento para o robô PUMA 560. Ele declara
    argumentos e nós necessários para configurar e visualizar o robô no ROS 2, incluindo
    a publicação do estado do robô e a interface gráfica de controle das juntas.
    
    Retorna:
        LaunchDescription: Um objeto contendo a configuração do lançamento.
  """

  """
  Declara um argumento de lançamento para o arquivo do modelo URDF/XACRO do robô.
  Este argumento permite definir o caminho absoluto para o arquivo XACRO do PUMA 560.
  É útil para que o arquivo URDF seja atualizado dinamicamente.
  """

  model_arg = DeclareLaunchArgument(
    name="model", 
    default_value=os.path.join(get_package_share_directory("puma560_description"),"urdf","puma560_description.urdf.xacro"),
    description = "Caminho absoluto para o arquivo URDF do robo"
  )

  """ 
  Cria o parâmetro `robot_description` que contém a descrição do robô.
  O comando 'xacro' é executado no arquivo XACRO especificado no argumento 'model',
  e o resultado é passado como a descrição do robô para o ROS.
  """

  robot_description = ParameterValue(
    Command(['xacro ', LaunchConfiguration('model')]), value_type=str
  )

  """ 
  Configura o nó `robot_state_publisher` para publicar o estado do robô.
  Este nó é responsável por ler a descrição do robô (URDF) e publicar os estados das juntas
  no tópico `tf`, permitindo que o ROS rastreie a posição de cada junta ao longo do tempo.
  """
  
  robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description}]
  )

  """
  Configura o nó `joint_state_publisher_gui`, que fornece uma interface gráfica
  para manipular as juntas do robô. Isso é útil para visualizar e controlar
  as posições das juntas manualmente durante a simulação.
  """

  joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
  )

  ''' Cometários '''

  rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", os.path.join(get_package_share_directory("puma560_description"),"rviz2","display_puma560.rviz")]
    )

  ''' Cometários '''

  return LaunchDescription([
      model_arg,
      robot_state_publisher_node, 
      joint_state_publisher_gui,
      rviz_node
  ])
