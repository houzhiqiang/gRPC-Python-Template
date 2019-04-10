build-proto:
	python3 -m grpc_tools.protoc -I./proto/service/bftoken --python_out=./service/protos/ --grpc_python_out=./service/protos/ ./proto/service/bftoken/bf_token.proto

start:
	python3 manage.py -c settings.ini

# celery 无法指定新的参数去配置service的参数，所以从环境变量读取
export INI_DIR=settings.ini
start-celery:
	celery -A service.bftoken_task.celery_app worker --loglevel=debug -P solo

start-celery-beat:
	celery -A service.bftoken_task.celery_app beat --loglevel=debug
