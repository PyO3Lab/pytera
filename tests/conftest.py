import pytest
import os
import pytera


@pytest.fixture(scope="session")
def template_dir():
    """返回模板目录路径"""
    return os.path.join(os.path.dirname(__file__), '..', 'templates')


@pytest.fixture(scope="session")
def tera_instance(template_dir):
    """创建共享的 PyTera 实例"""
    glob_pattern = f"{template_dir}/*.html"
    return pytera.PyTera(glob_pattern)


@pytest.fixture
def sample_data():
    """提供测试用的示例数据"""
    return {
        "name": "Alice",
        "age": 30,
        "user": {"name": "Bob", "is_admin": True},
        "items": [
            {"name": "Apple", "price": 1.234},
            {"name": "Banana", "price": 0.567},
            {"name": "Orange", "price": 2.891}
        ],
        "text": "hello world",
        "list": ["a", "b", "c", "d", "e"],
        "site_name": "My Site"
    }