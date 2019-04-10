"""初始化"""
import os
import sys
import time

from concurrent import futures

import grpc
import sentry_sdk

from sqlalchemy import create_engine

# from client.asset import Asset
from configs import basedir
from configs import config

from .log import init_log
from .log import logging
from .utils import ImmutableDict
from .utils.config import Config


# pylint: disable=W0107


class App():
    """用于创建应用实例"""
    config_class = Config
    default_config = ImmutableDict({
        # 'TIMEZONE': 'UTC',
        'WORKERS': 4,
        'HOST': '[::]',
        'PORT': 6000,
    })

    def __init__(self, root_path, service=None):
        if not os.path.isabs(root_path):
            root_path = os.path.abspath(root_path)
        self.root_path = root_path
        self.name = os.path.basename(root_path)
        self.config = self.config_class(root_path, self.default_config)
        self.service = service

    def add_service(self, service):
        """注册service"""
        if self.service is None:
            self.service = service
        self.service.update(service)

    def start(self):
        """start server"""
        server = grpc.server(
            futures.ThreadPoolExecutor(
                max_workers=self.config["WORKERS"]
            )
        )

        if self.service is None or not self.service:
            raise NotService("not service")

        for k, v in self.service.items():
            k(v(), server)

        server.add_insecure_port(
            f'{self.config["HOST"]}:{self.config["PORT"]}'
        )
        server.start()
        try:
            while True:
                time.sleep(self.config["_ONE_DAY_IN_SECONDS"])
        except KeyboardInterrupt:
            server.stop(0)


class NotService(Exception):
    """没有注册service"""
    pass


def create_app(config_name=None):
    """create app"""
    app_ = App(basedir)
    # 初始化配置
    if os.getenv("INI_DIR"):
        # celery 使用交易服务相关模块的配置(DB, MQ)
        config["default"].init(os.getenv("INI_DIR"))
        app_.config.from_object(config["default"])
        return app_

    if "-c" in config_name:
        config["default"].init(config_name[config_name.index("-c") + 1])
        app_.config.from_object(config["default"])
    else:
        config_name = os.getenv("CONFIG_NAME")
        if not config_name:
            sys.exit("请设置 CONFIG_NAME 环境变量 或 使用 -c 参数指定配置文件")
        app_.config.from_object(config[config_name])
    return app_


app = create_app(config_name=sys.argv)

# 提供有效的DSN配置 初始化 sentry_sdk
if app.config["DSN"]:
    sentry_sdk.init(app.config["DSN"])

init_log(
    app.config['LOG_FILE_NAME'],
    app.config['LOG_LEVEL'],
    app.config['LOG_INPUT_POSITION']
)

logger = logging.getLogger("main")
logger.info("bftoken app start")
logger.info(f'config_name: {os.getenv("CONFIG_NAME")}')


engine_bftoken = create_engine(
    app.config["SQL_DB_BFTOKEN_URI"],
    echo=app.config["SQL_DEBUG"],
    pool_recycle=app.config['POOL_RECYCLE'],
    max_overflow=app.config['SQLALCHEMY_MAX_OVERFLOW'],
    pool_size=app.config['SQLALCHEMY_POOL_SIZE'],
)

# asset_client = Asset(app.config["ASSET_CLIENT_IP"],
#                      app.config["ASSET_CLIENT_PORT"])
