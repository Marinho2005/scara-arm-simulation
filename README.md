# SCARA Arm Simulation

**Discentes:** João Vitor Ramos Burgos, Victor Marinho Borges da Silva Lima

Projeto ROS 2 para visualizar e simular um braco SCARA com garra de dois dedos. A demonstracao move o braco suavemente, fecha a garra durante a descida e retorna ao ponto inicial. Ela e apenas gestual: nao ha uma bola ou outro objeto sendo agarrado.

Este roteiro usa **Bash**. A unica diferenca em relacao ao Zsh e trocar `setup.bash` por `setup.zsh` nos comandos de `source`. Todo o resto e identico.

## Requisitos

- Ubuntu 22.04
- ROS 2 Humble Desktop
- Gazebo Classic com os pacotes ROS 2 para Gazebo
- Terminator
- Conexao com a internet durante a instalacao das dependencias

Se ainda nao tiver ROS 2 Humble Desktop, siga primeiro o guia oficial de instalacao para Ubuntu 22.04:
https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html

## Passo 0: confirme que esta no Bash

```bash
echo $SHELL
```

Se aparecer `/bin/bash`, siga em frente. Se aparecer `/usr/bin/zsh`, digite `bash` na aba antes de rodar os comandos:

```bash
bash
```

## Passo 1: instalar as ferramentas

```bash
sudo apt update
sudo apt install terminator python3-colcon-common-extensions python3-rosdep
```

## Passo 2: criar o workspace e baixar o codigo

```bash
mkdir -p ~/scara_ws/src
cd ~/scara_ws/src
git clone https://github.com/Marinho2005/scara-arm-simulation
```

Se o codigo ja estiver em `~/scara_ws/src/scara-arm-simulation`, nao clone de novo. Va direto para o passo 3.

## Passo 3: instalar as dependencias e compilar

```bash
unset AMENT_PREFIX_PATH COLCON_PREFIX_PATH CMAKE_PREFIX_PATH
source /opt/ros/humble/setup.bash
cd ~/scara_ws
```

Inicialize o rosdep somente se ainda nao tiver sido inicializado neste computador. Se `sudo rosdep init` disser que ja existe uma configuracao, ignore a mensagem e continue:

```bash
sudo rosdep init
rosdep update
```

Instale as dependencias declaradas pelos pacotes e compile:

```bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
```

O resultado esperado do build e `Summary: 2 packages finished`.

## Passo 4: rodar no Terminator

Abra o Terminator pelo menu de aplicativos e crie tres abas com `Ctrl+Shift+T`.

Em **cada aba**, carregue o ambiente:

```bash
unset AMENT_PREFIX_PATH COLCON_PREFIX_PATH CMAKE_PREFIX_PATH
source /opt/ros/humble/setup.bash
source ~/scara_ws/install/setup.bash
```

### Aba 1: Gazebo

Inicie o mundo e espere o Gazebo abrir e o robo aparecer:

```bash
ros2 launch scara_description gazebo.launch.py
```

### Aba 2: Controladores

Depois que o robo aparecer no Gazebo, use a segunda aba:

```bash
ros2 launch scara_controller controller.launch.py
```

Espere os controladores `arm_controller` e `gripper_controller` informarem que estao ativos.

### Aba 3: Demonstracao

Quando o Gazebo e os controladores estiverem rodando, use a terceira aba:

```bash
/usr/bin/python3 ~/scara_ws/src/scara-arm-simulation/demo.py
```

A garra abre, o braco desce e fecha a garra como se pegasse algo, sobe e volta ao home. Como nao existe objeto na cena, a demonstracao nao realiza uma pegada fisica.

Para encerrar, pressione `Ctrl+C` nas abas da demonstracao, dos controladores e do Gazebo.

## Passo 5: visualizar no RViz (opcional)

O RViz com sliders e uma visualizacao separada do Gazebo. Carregue o ambiente em uma aba, como no passo 4, e rode:

```bash
ros2 launch scara_description scara.launch.py
```

## Solucao de problemas

**`Package not found` ou `ros2: command not found`:** recarregue o ambiente na aba atual:

```bash
unset AMENT_PREFIX_PATH COLCON_PREFIX_PATH CMAKE_PREFIX_PATH
source /opt/ros/humble/setup.bash
source ~/scara_ws/install/setup.bash
```

**Comandos com `setup.zsh` falham:** confirme que voce digitou `bash` na aba e troque todos os `setup.zsh` por `setup.bash`. Nao misture os dois arquivos no mesmo terminal.

**O pacote nao aparece depois de alterar o codigo:** pare os nos com `Ctrl+C`, compile novamente a partir da raiz do workspace e carregue o overlay:

```bash
cd ~/scara_ws
colcon build --symlink-install
source install/setup.bash
```

**Gazebo ou controladores ja estavam abertos durante o build:** encerre as instancias antigas e inicie novamente as abas 1 e 2. Um processo em execucao nao carrega automaticamente as alteracoes feitas nos arquivos.

**O Gazebo abre sem janela ou o cliente grafico fecha:** confirme que a sessao grafica do Ubuntu esta ativa e que `DISPLAY` esta definido. O servidor Gazebo pode continuar rodando mesmo se a janela grafica fechar.
