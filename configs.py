"""项目配置文件"""
import logging
import os
import sys

from configparser import ConfigParser

# pylint: disable=R0903, W0107


basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    """默认"""
    HOST = '0.0.0.0'
    PORT = 10040
    WORKERS = os.cpu_count() * 2
    _ONE_DAY_IN_SECONDS = 60 * 60 * 24

    GLOBAL_DATABASE_HOST = '10.10.10.56'
    GLOBAL_DATABASE_USER = "root"
    GLOBAL_DATABASE_PASS = ""

    SQL_DB_BFTOKEN_URI = (
        f"mysql+pymysql://{GLOBAL_DATABASE_USER}:{GLOBAL_DATABASE_PASS}"
        f"@{GLOBAL_DATABASE_HOST}:3306/bf_bfold?charset=utf8mb4"
    )
    SQL_DEBUG = True
    POOL_RECYCLE = 3600

    ASSET_CLIENT_IP = "10.10.10.57"
    ASSET_CLIENT_PORT = "10030"

    LOG_FILE_NAME = "./log/trade"
    LOG_LEVEL = logging.INFO
    LOG_INPUT_POSITION = ['file', 'console']
    # SQLALCHEMY_LOG_INPUT_POSITION = ['file', 'console']
    SQLALCHEMY_MAX_OVERFLOW = 20
    SQLALCHEMY_POOL_SIZE = 20

    MQ_HOST = "10.10.10.56"
    MQ_USER_PORT = 5672
    MQ_USER_NAME = "guest"
    MQ_PASSWORD = ""

    DSN = ""

    @classmethod
    def init(cls, path):
        """从ini配置文件覆盖基本配置"""
        LEVEL = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARN": logging.WARN,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }

        configs = ConfigParser()
        configs.read(path, encoding="UTF-8")
        setattr(cls, "HOST", configs.get("grpc", "GRPC_HOST"))
        setattr(cls, "PORT", configs.get("grpc", "GRPC_PORT"))
        setattr(cls, "WORKERS", configs.getint("grpc", "GRPC_WORKERS"))
        setattr(
            cls, "SQL_DB_BFTOKEN_URI",
            f"mysql+pymysql://{configs.get('mysql', 'BF_BFTOKEN_USER')}:{configs.get('mysql', 'BF_BFTOKEN_PASS')}"
            f"@{configs.get('mysql', 'BF_BFTOKEN_HOST')}/bf_bfold?charset=utf8mb4"
        )
        setattr(cls, "SQL_DEBUG", configs.getboolean("sqlalchemy", "DEBUG"))
        setattr(cls, "POOL_RECYCLE", configs.getint("sqlalchemy", "POOL_RECYCLE"))
        setattr(cls, "SQLALCHEMY_MAX_OVERFLOW", configs.getint("sqlalchemy", "MAX_OVERFLOW"))
        setattr(cls, "SQLALCHEMY_POOL_SIZE", configs.getint("sqlalchemy", "POOL_SIZE"))
        setattr(cls, "ASSET_CLIENT_IP", configs.get("client", "ASSET_HOST"))
        setattr(cls, "ASSET_CLIENT_PORT", configs.get("client", "ASSET_PORT"))
        setattr(cls, "MQ_HOST", configs.get("rabbit", "MQ_HOST"))
        setattr(cls, "MQ_USER_PORT", configs.get("rabbit", "MQ_PORT"))
        setattr(cls, "MQ_USER_NAME", configs.get("rabbit", "MQ_USER_NAME"))
        setattr(cls, "MQ_PASSWORD", configs.get("rabbit", "MQ_PASS"))
        setattr(cls, "DSN", configs.get("sentry", "DSN"))
        setattr(cls, "LOG_LEVEL", LEVEL[configs.get("log", "LEVEL")])
        setattr(cls, "LOG_FILE_NAME", configs.get("log", "DIR"))
        if configs.getboolean("log", "IS_CONSOLE") and configs.getboolean("log", "IS_FILE"):
            setattr(cls, "LOG_INPUT_POSITION", ['file', 'console'])
        elif configs.getboolean("log", "IS_CONSOLE"):
            setattr(cls, "LOG_INPUT_POSITION", ['console', ])
        elif configs.getboolean("log", "IS_FILE"):
            setattr(cls, "LOG_INPUT_POSITION", ['file', ])
        else:
            sys.exit("请确认日志输出路径")


class DevelopmentConfig(Config):
    """开发"""
    SQLALCHEMY_MAX_OVERFLOW = 20
    SQLALCHEMY_POOL_SIZE = 20
    SQL_DEBUG = False  # "debug"
    WORKERS = 100
    LOG_LEVEL = logging.DEBUG
    LOG_INPUT_POSITION = ['file', 'console']
    SQLALCHEMY_LOG_INPUT_POSITION = ['file', 'console']


class TestingConfig(Config):
    """测试"""
    GLOBAL_DATABASE_HOST = '10.10.10.50'
    GLOBAL_DATABASE_USER = "hicar"
    GLOBAL_DATABASE_PASS = ""

    SQL_DB_BFTOKEN_URI = (
        f"mysql+pymysql://{GLOBAL_DATABASE_USER}:{GLOBAL_DATABASE_PASS}"
        f"@{GLOBAL_DATABASE_HOST}:3306/bf_bfold?charset=utf8mb4"
    )

    WORKERS = 2
    port = 1040
    SQL_DEBUG = False
    LOG_FILE_NAME = "./log/trade"
    LOG_LEVEL = logging.DEBUG
    SQLALCHEMY_LOG_INPUT_POSITION = ['console']
    LOG_INPUT_POSITION = ['console']


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': Config,
}
