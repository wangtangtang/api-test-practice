"""DummyJSON 接口封装层 - https://dummyjson.com/"""
import requests
from utils.logger import get_logger

logger = get_logger(__name__)


class DummyJsonClient:
    """https://dummyjson.com/ 公开练习 API client（电商场景：用户/商品/购物车）"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    # ---------- 通用方法 ----------
    def _post(self, path: str, payload: dict) -> requests.Response:
        url = f"{self.base_url}{path}"
        logger.info(f"POST {url} | payload={payload}")
        resp = self.session.post(url, json=payload)
        logger.info(f"  <- {resp.status_code} | body={resp.text[:200]}")
        return resp

    def _get(self, path: str, params: dict = None) -> requests.Response:
        url = f"{self.base_url}{path}"
        logger.info(f"GET {url} | params={params}")
        resp = self.session.get(url, params=params)
        logger.info(f"  <- {resp.status_code} | body={resp.text[:200]}")
        return resp

    # ---------- 业务方法 ----------
    def login(self, username: str = None, password: str = None) -> requests.Response:
        """用户登录"""
        payload = {}
        if username is not None:
            payload["username"] = username
        if password is not None:
            payload["password"] = password
        return self._post("/auth/login", payload)

    def list_products(self, limit: int = 30, skip: int = 0) -> requests.Response:
        """商品列表（电商挂载场景）"""
        return self._get("/products", params={"limit": limit, "skip": skip})

    def get_product(self, product_id: int) -> requests.Response:
        """商品详情"""
        return self._get(f"/products/{product_id}")

    def get_cart(self, cart_id: int) -> requests.Response:
        """获取购物车详情（对应直播间购物车业务）"""
        return self._get(f"/carts/{cart_id}")

    def list_carts(self) -> requests.Response:
        """所有购物车列表"""
        return self._get("/carts")
