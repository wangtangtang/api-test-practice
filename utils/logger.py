"""全局日志工具"""
import logging
import sys


def get_logger(name: str = "api-test") -> logging.Logger:
    """获取统一格式的 logger，避免重复添加 handler"""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    )
    logger.addHandler(handler)
    logger.propagate = False
    return logger
