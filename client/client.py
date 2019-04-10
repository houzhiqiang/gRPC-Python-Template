"""
client demo

联调用客户端
"""
import grpc

from protos import bf_token_pb2_grpc
from protos import bf_token_pb2


def test_bf():
    """"平台币"""
    with grpc.insecure_channel('localhost:10040') as channel:
        stub = bf_token_pb2_grpc.BfTokenStub(channel)
        res = stub.GetBfAsset(bf_token_pb2.GetBfAssetRequest(user_id=43))
        print(res)
        res = stub.GetUserMiningStatistics(
            bf_token_pb2.GetUserMiningStatisticsRequest(
                user_id=43
            )
        )
        print(":::::::::==============================> ", res)
