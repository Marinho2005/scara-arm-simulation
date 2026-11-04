#!/usr/bin/env python3
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

class ScaraDemoNode(Node):
    def __init__(self):
        super().__init__('scara_demo_node')
        self.arm_command_publisher = self.create_publisher(
            Float64MultiArray, '/arm_controller/commands', 10
        )
        self.gripper_command_publisher = self.create_publisher(
            Float64MultiArray, '/gripper_controller/commands', 10
        )
        self.current_arm_positions = [0.0, 0.0, 0.0, 0.0]
        time.sleep(1.0)
        self.get_logger().info("Iniciando a demonstracao gestual de pega, sem objeto...")

    def publish_arm(self, target_positions, duration=3.0):
        start_positions = self.current_arm_positions
        sample_count = max(int(duration * 20), 1)

        for sample in range(1, sample_count + 1):
            progress = sample / sample_count
            eased_progress = progress * progress * (3.0 - 2.0 * progress)
            msg = Float64MultiArray()
            msg.data = [
                start + (target - start) * eased_progress
                for start, target in zip(start_positions, target_positions)
            ]
            self.arm_command_publisher.publish(msg)
            time.sleep(duration / sample_count)

        self.current_arm_positions = list(target_positions)

    def publish_gripper(self, opening):
        msg = Float64MultiArray()
        msg.data = [opening]
        for _ in range(10):
            self.gripper_command_publisher.publish(msg)
            time.sleep(0.1)

    def run_sequence(self):
        self.get_logger().info('1. Abrir a garra')
        self.publish_gripper(0.3)

        self.get_logger().info('2. Posicionar acima do ponto de pega')
        self.publish_arm([0.8, -1.2, 0.0, 0.0], duration=4.0)
        time.sleep(1.0)

        self.get_logger().info('3. Descer e fechar a garra como se pegasse algo')
        self.publish_arm([0.8, -1.2, -0.07, 0.0], duration=2.5)
        self.publish_gripper(0.0)
        time.sleep(0.8)

        self.get_logger().info('4. Erguer e voltar com a garra fechada')
        self.publish_arm([0.8, -1.2, -0.01, 0.0], duration=2.5)
        self.publish_arm([0.0, 0.0, -0.01, 0.0], duration=4.0)

        self.get_logger().info('5. Baixar e abrir a garra no home')
        self.publish_arm([0.0, 0.0, 0.0, 0.0], duration=1.5)
        self.publish_gripper(0.3)
        self.get_logger().info('Demonstracao gestual concluida; nenhum objeto foi agarrado.')

def main(args=None):
    rclpy.init(args=args)
    node = ScaraDemoNode()
    try:
        node.run_sequence()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
