"""购物车接口测试 - GET /carts
对应直播间购物车场景：用户购物车查询、商品挂载校验"""
import pytest
from api.dummyjson_client import DummyJsonClient


@pytest.fixture
def client(base_url):
    return DummyJsonClient(base_url)


class TestCarts:
    """覆盖：列表正向 + 详情字段校验 + 金额计算逻辑 + 404"""

    @pytest.mark.smoke
    def test_list_all_carts(self, client):
        """正向：拉取所有购物车，校验结构"""
        response = client.list_carts()

        assert response.status_code == 200
        body = response.json()
        assert "carts" in body and isinstance(body["carts"], list)
        assert body["total"] > 0
        assert len(body["carts"]) > 0

    def test_get_cart_detail(self, client):
        """正向：查询购物车详情，校验商品挂载字段"""
        response = client.get_cart(cart_id=1)

        assert response.status_code == 200
        cart = response.json()
        # 关键字段断言
        assert cart["id"] == 1
        assert "products" in cart and len(cart["products"]) > 0
        assert "totalProducts" in cart
        assert "totalQuantity" in cart
        # 每个购物车商品的关键字段（直播间挂载关心的字段）
        for item in cart["products"]:
            assert "id" in item
            assert "title" in item
            assert "price" in item and item["price"] >= 0
            assert "quantity" in item and item["quantity"] > 0

    def test_cart_total_calculation(self, client):
        """业务逻辑校验：购物车总金额 = 所有商品 price*quantity 之和（折扣后）"""
        response = client.get_cart(cart_id=1)

        assert response.status_code == 200
        cart = response.json()
        # 折扣后总价应小于等于原始总价
        assert cart["discountedTotal"] <= cart["total"], \
            f"折扣价 {cart['discountedTotal']} 应 ≤ 原价 {cart['total']}"
        # totalQuantity 应等于所有商品 quantity 之和
        sum_quantity = sum(p["quantity"] for p in cart["products"])
        assert cart["totalQuantity"] == sum_quantity, \
            f"totalQuantity 应等于商品 quantity 之和：{cart['totalQuantity']} vs {sum_quantity}"

    def test_get_cart_not_found(self, client):
        """异常：查询不存在的购物车 ID，返回 404"""
        response = client.get_cart(cart_id=9999)

        assert response.status_code == 404
        body = response.json()
        assert "message" in body
        assert "not found" in body["message"].lower()
