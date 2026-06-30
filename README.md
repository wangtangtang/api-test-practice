# API Test Practice

> 个人接口自动化练习项目，基于 `requests + pytest`，测试公开的 fake 电商 API [dummyjson.com](https://dummyjson.com/)。
> 选 dummyjson 是因为它的 **用户/商品/购物车** 三类接口贴近直播电商业务（商品挂载、购物车展示），可以把以往的功能测试经验自然迁移到接口层。

## 项目目的

- 巩固 Python + Requests + Pytest 接口测试基本流程
- 覆盖常见用例类型：正向路径、参数错误、字段三层校验、数据驱动、业务逻辑断言
- 沉淀可复用的请求封装、日志、配置结构，便于后续扩展到真实业务

## 环境要求

- Python 3.8+
- pip
- 可访问外网（用于请求 dummyjson.com）

## 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/<your-name>/api-test-practice.git
cd api-test-practice

# 2.（可选）建立虚拟环境
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 跑全部测试
pytest -v

# 5. 跑冒烟用例（核心正向路径）
pytest -v -m smoke

# 6. 生成 HTML 报告
pytest --html=reports/report.html --self-contained-html
```

## 目录结构

```
api-test-practice/
├── api/                       # 业务接口封装层
│   └── dummyjson_client.py    # DummyJSON 的 client（请求方法 + 日志）
├── testcases/                 # 测试用例
│   ├── test_user_login.py     # 登录接口
│   ├── test_products.py       # 商品列表/详情
│   └── test_carts.py          # 购物车
├── utils/                     # 工具类
│   └── logger.py              # 统一 logger
├── reports/                   # 测试报告输出
├── conftest.py                # pytest fixture
├── pytest.ini                 # pytest 配置
└── requirements.txt
```

## 用例覆盖

| 文件 | 用例数 | 覆盖类型 |
|---|---|---|
| `test_user_login.py` | 3 | 正向登录、密码错误、缺失参数 |
| `test_products.py`   | 6 | 列表正向 + 字段校验 + 分页（3 组数据驱动）+ 详情 + 404 |
| `test_carts.py`      | 4 | 列表正向 + 详情字段 + 业务逻辑（金额/数量计算）+ 404 |

**合计 13 个用例**，跑通约 3-5 秒。

## 设计思路

1. **三层分层** — API 封装 / 测试用例 / 工具，便于扩展和复用
2. **配置外置** — `base_url` 通过 conftest 的 fixture 注入，切换环境只改一处
3. **断言三层校验** — 状态码 → 关键字段存在 → 业务规则（如折扣价 ≤ 原价、quantity 之和正确）
4. **数据驱动** — 用 `pytest.mark.parametrize` 一次覆盖多组数据，避免复制粘贴
5. **日志可追溯** — 每个请求记录 URL + payload + 响应，失败排查不靠猜

## 后续规划

- [ ] 接入 Allure 报告（更直观，面试看着舒服）
- [ ] 接入 GitHub Actions CI（push 自动跑测试，README 加 badge）
- [ ] 加入接口性能基线监测（响应时间断言）
- [ ] 扩展到真实业务模拟（mock 一个完整电商下单链路）

## 作者

10 年功能测试经验，正在把"了解"的自动化能力沉淀成实战。
