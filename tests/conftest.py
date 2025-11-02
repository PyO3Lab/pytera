from __future__ import annotations

from pathlib import Path

import pytest

from pytera import PyTera

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


@pytest.fixture(scope="session")
def template_dir() -> Path:
    return TEMPLATES_DIR


@pytest.fixture(scope="session")
def tera_instance(template_dir: Path) -> PyTera:
    glob_pattern = str(template_dir / "*.html")
    return PyTera(glob_pattern)


@pytest.fixture
def admin_user() -> dict[str, object]:
    return {"name": "Bob", "is_admin": True}


@pytest.fixture
def regular_user() -> dict[str, object]:
    return {"name": "Charlie", "is_admin": False}


@pytest.fixture
def site_name() -> str:
    return "My Site"


@pytest.fixture
def inventory_items() -> list[dict[str, float]]:
    return [
        {"name": "Apple", "price": 1.234},
        {"name": "Banana", "price": 0.567},
        {"name": "Orange", "price": 2.891},
    ]


@pytest.fixture
def filter_context() -> dict[str, object]:
    return {
        "text": "hello world",
        "missing": None,
        "list": ["a", "b", "c", "d", "e"],
    }