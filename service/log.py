"""日志处理器"""
import datetime
import logging
import os

from logging.config import dictConfig


def init_log(filename, level=logging.INFO, input_position=None):
    """初始化日志配置"""
    if input_position is None:
        input_position = ['file', 'console']

    handlers = {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': level,
        },
    }

    if 'file' in input_position:
        handlers.update({
            'file': {
                'class': 'logging.FileHandler',
                'filename': f'{filename}_{datetime.datetime.now()}_{os.getpid()}.log',
                'formatter': 'default',
                'level': level,
            },
        })

    logging_config = dict(
        version=1,
        formatters={
            'default': {
                'format': '%(asctime)s %(levelname)-8s %(name)-15s %(message)s'
            }
        },
        filter={
        },
        handlers=handlers,
        loggers={
            'main': {
                'handlers': input_position,
                'level': level,
                "encoding": "utf8"
            },
            'db': {
                'handlers': input_position,
                'level': level,
                "encoding": "utf8"
            },
            'bftoken': {
                'handlers': input_position,
                'level': level,
                "encoding": "utf8"
            },
        }
    )

    dictConfig(logging_config)
