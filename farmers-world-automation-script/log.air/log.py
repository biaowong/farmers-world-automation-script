# -*- encoding=utf8 -*-
"""
日志相关定义
"""

import logging
from airtest.core.api import *

using("config.air")
import config

# pylint: disable=C0103
# 创建 logger，如果参数为空则赶回 root logger
logger = logging.getLogger('farmers_world')

# 动态设置日志等级
config_log_level = config.LOG_LEVEL if hasattr(config, 'LOG_LEVEL') else 'INFO'
log_level = getattr(logging, config_log_level)
logger.setLevel(log_level) # 设置 logger 日志等级

logger.propagate = False

# 设置日志输出格式
formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(filename)s %(lineno)s: %(message)s",
    datefmt="%Y-%m-%d %X"
)

# 创建 handler
# fh = logging.FileHandler("farmers_world.log", encoding="utf-8")
ch = logging.StreamHandler()

# 为 handler 指定输出格式
# fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 为 logger 添加日志处理器
# logger.handlers.append(fh)
logger.handlers.append(ch)


