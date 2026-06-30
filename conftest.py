"""pytest 全局 fixture"""
import pytest
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="session")
def base_url():
    """API 基础 URL，切换环境改这里即可"""
    return "https://dummyjson.com"


@pytest.fixture(autouse=True)
def log_test_info(request):
    """每个用例前后打印日志，便于失败排查"""
    logger.info(f"========== START: {request.node.name} ==========")
    yield
    logger.info(f"========== END:   {request.node.name} ==========\n")
