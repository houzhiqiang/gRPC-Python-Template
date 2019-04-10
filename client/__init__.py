"""暴露rpc方法 用于单元测试"""
import grpc


# pylint: disable=R0903


class ClientBase:
    """客户端基类"""
    def __init__(self, host, port):
        self.channel = grpc.insecure_channel(f"{host}:{port}")

    def init_app(self, host, port):
        """从app 初始化"""
        self.channel = grpc.insecure_channel(f"{host}:{port}")
