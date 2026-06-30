"""商品列表与详情接口测试 - GET /products
对应电商挂载场景：商品库展示、详情查询"""
import pytest
from api.dummyjson_client import DummyJsonClient


@pytest.fixture
def client(base_url):
    return DummyJsonClient(base_url)


class TestProducts:
    """覆盖：列表正向 + 字段断言 + 分页 + 详情 + 404"""

    @pytest.mark.smoke
    def test_list_products_default(self, client):
        """正向：默认拉取商品列表，校验关键字段"""
        response = client.list_products(limit=5)

        assert response.status_code == 200
        body = response.json()
        # 三层校验：结构 + 类型 + 业务
        assert "products" in body and isinstance(body["products"], list)
        assert len(body["products"]) == 5, "limit=5 应返回 5 条"
        assert body["total"] > 0
        # 商品字段断言（对应直播间挂载场景的关键字段）
        for product in body["products"]:
            assert "id" in product
            assert "title" in product and len(product["title"]) > 0
            assert "price" in product and product["price"] >= 0, f"价格应非负: {product['price']}"
            assert "category" in product

    @pytest.mark.parametrize("limit,skip,expected_count", [
        (10, 0, 10),    # 第 1 页 10 条
        (5, 10, 5),     # 跳过 10 条后取 5 条
        (3, 0, 3),      # 小批量
    ])
    def test_list_products_pagination(self, client, limit, skip, expected_count):
        """数据驱动：分页参数生效"""
        response = client.list_products(limit=limit, skip=skip)

        assert response.status_code == 200
        body = response.json()
        assert len(body["products"]) == expected_count
        assert body["skip"] == skip
        assert body["limit"] == limit

    def test_get_product_detail(self, client):
        """正向：查询商品详情，校验字段完整性"""
        response = client.get_product(product_id=1)

        assert response.status_code == 200
        product = response.json()
        assert product["id"] == 1
        # 详情比列表多的字段
        assert "description" in product
        assert "stock" in product and product["stock"] >= 0
        assert "rating" in product

    def test_get_product_not_found(self, client):
        """异常：查询不存在的商品 ID，返回 404"""
        response = client.get_product(product_id=99999)

        assert response.status_code == 404
        body = response.json()
        assert "message" in body
        assert "not found" in body["message"].lower()
