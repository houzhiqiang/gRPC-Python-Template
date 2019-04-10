"""资产 客户端"""
from decimal import Decimal

# from protos import asset_pb2
# from protos import asset_pb2_grpc

from .. import ClientBase


class ClientDemo(ClientBase):
    """资产客户端"""
    def __init__(self, host, port):
        super().__init__(host, port)
        # self.stub = asset_pb2_grpc.UserAssetStub(self.channel)

    def demo(self):
        pass
