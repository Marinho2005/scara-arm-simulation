# SCARA Arm Simulation

Projeto ROS 2 para visualizar e simular um braco SCARA com garra de dois dedos. A demonstracao move o braco suavemente, fecha a garra durante a descida e retorna ao ponto inicial. Ela e apenas gestual: nao ha uma bola ou outro objeto sendo agarrado.



## Requisitos

- Ubuntu 22.04
- ROS 2 Humble Desktop
- Gazebo Classic com os pacotes ROS 2 para Gazebo
- Terminator
- Conexao com a internet durante a instalacao das dependencias

Os comandos abaixo usam Zsh, que e o shell configurado neste computador. Abra os terminais novos pelo Terminator para reproduzir os passos.

## Instalar ferramentas

Se ROS 2 Humble ja estiver instalado, abra um terminal e instale as ferramentas usadas pelo workspace:

```zsh
sudo apt update
sudo apt install terminator python3-colcon-common-extensions python3-rosdep
```

Se ainda nao tiver ROS 2 Humble Desktop, siga primeiro o guia oficial de instalacao para Ubuntu 22.04:
https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html

## Criar o workspace e baixar o codigo

Crie as pastas e clone o repositorio de origem:

```zsh
mkdir -p ~/scara_ws/src
cd ~/scara_ws/src
git clone https://github.com/Marinho2005/scara-arm-simulation

Se o codigo ja estiver em `~/scara_ws/src/scara-arm-simulation`, nao clone de novo. Va direto para a instalacao das dependencias.

## Instalar dependencias e compilar

Execute no mesmo terminal:

```zsh
unset AMENT_PREFIX_PATH COLCON_PREFIX_PATH CMAKE_PREFIX_PATH
source /opt/ros/humble/setup.zsh
cd ~/scara_ws
```

Inicialize o rosdep somente se ainda nao tiver sido inicializado neste computador. Se `sudo rosdep init` disser que ja existe uma configuracao, ignore essa mensagem e continue:

```zsh
sudo rosdep init
rosdep update
```

Instale as dependencias declaradas pelos pacotes e compile:

```zsh
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
```

O resultado esperado do build e `Summary: 2 packages finished`. Sempre que abrir uma nova aba do Terminator, carregue o ROS e o workspace com os comandos da proxima secao.

## Rodar no Terminator

Abra o Terminator pelo menu de aplicativos. Crie tres abas com `Ctrl+Shift+T`. Rode um bloco de comandos por aba e mantenha as tres abertas. Em cada aba, primeiro carregue o ambiente:

```zsh
unset AMENT_PREFIX_PATH COLCON_PREFIX_PATH CMAKE_PREFIX_PATH
source /opt/ros/humble/setup.zsh
source ~/scara_ws/install/setup.zsh
```

### Aba 1: Gazebo

Na primeira aba, inicie o mundo e espere o Gazebo abrir e o robo aparecer:

```zsh
ros2 launch scara_description gazebo.launch.py
```

### Aba 2: Controladores

Depois que o robo aparecer no Gazebo, use a segunda aba:

```zsh
ros2 launch scara_controller controller.launch.py
```

Espere os controladores `arm_controller` e `gripper_controller` informarem que estao ativos.

### Aba 3: Demonstracao

Quando o Gazebo e os controladores estiverem rodando, use a terceira aba:

```zsh
/usr/bin/python3 ~/scara_ws/src/scara-arm-simulation/demo.py
```

A garra abre, o braco desce e fecha a garra como se pegasse algo, sobe e volta ao home. Como nao existe objeto na cena, a demonstracao nao realiza uma pegada fisica.

Para encerrar, pressione `Ctrl+C` nas abas da demonstracao, dos controladores e do Gazebo.

## Visualizar no RViz

O RViz com sliders e uma visualizacao separada do Gazebo. Carregue o ambiente em uma aba e rode:

```zsh
ros2 launch scara_description scara.launch.py
```

## Solucao de problemas

**`Package not found` ou `ros2: command not found`:** recarregue o ambiente na aba atual:

```zsh
unset AMENT_PREFIX_PATH COLCON_PREFIX_PATH CMAKE_PREFIX_PATH
source /opt/ros/humble/setup.zsh
source ~/scara_ws/install/setup.zsh
```

**O pacote nao aparece depois de alterar o codigo:** pare os nos com `Ctrl+C`, compile novamente a partir da raiz do workspace e carregue o overlay:

```zsh
cd ~/scara_ws
colcon build --symlink-install
source install/setup.zsh
```

**Gazebo ou controladores ja estavam abertos durante o build:** encerre as instancias antigas e inicie novamente as abas 1 e 2. Um processo em execucao nao carrega automaticamente as alteracoes feitas nos arquivos.

**O Gazebo abre sem janela ou o cliente grafico fecha:** confirme que a sessao grafica do Ubuntu esta ativa e que `DISPLAY` esta definido. O servidor Gazebo pode continuar rodando mesmo se a janela grafica fechar.
