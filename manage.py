"""manage"""
# from gevent import monkey; monkey.patch_all(thread=False)
# import grpc.experimental.gevent
# grpc.experimental.gevent.init_gevent()
from service import app

# from service.protos import bf_token_pb2_grpc
# from service.bftoken import bftoken


service = {
    # bf_token_pb2_grpc.add_BfTokenServicer_to_server: bftoken.BfToken,
}

print(app.config)
# 注册service
app.add_service(service)
print("start")
# start 之后程序将阻塞(主线程)
app.start()
