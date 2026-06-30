"""用户登录接口测试 - POST /auth/login"""
import pytest
from api.dummyjson_client import DummyJsonClient


@pytest.fixture
def client(base_url):
    return DummyJsonClient(base_url)


class TestUserLogin:
    """覆盖：正向 + 错误密码 + 缺失参数"""

    @pytest.mark.smoke
    def test_login_success(self, client):
        """正向：合法用户名密码登录，返回 accessToken 和用户信息"""
        response = client.login(username="emilys", password="emilyspass")

        assert response.status_code == 200, f"期望 200，实际 {response.status_code}"
        body = response.json()
        assert "accessToken" in body, "返回体应包含 accessToken"
        assert isinstance(body["accessToken"], str) and len(body["accessToken"]) > 0
        # 业务字段校验
        assert body["username"] == "emilys"
        assert "@" in body["email"]

    def test_login_wrong_password(self, client):
        """异常：密码错误，返回 400"""
        response = client.login(username="emilys", password="wrong_password_123")

        assert response.status_code == 400
        body = response.json()
        assert "message" in body
        assert "invalid" in body["message"].lower() or "wrong" in body["message"].lower()

    def test_login_missing_password(self, client):
        """异常：缺少 password 参数，返回 400"""
        response = client.login(username="emilys")

        assert response.status_code == 400
        body = response.json()
        assert "message" in body
