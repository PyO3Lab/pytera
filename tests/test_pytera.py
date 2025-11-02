from __future__ import annotations

import html
import pytest

from pytera import PyTera, PyTeraRenderException


def test_basic_variables_renders_context(tera_instance: PyTera) -> None:
    result = tera_instance.render_template(
        "basic_variables.html",
        name="Alice",
        age=30,
    )
    assert result.strip() == "Hello Alice! You are 30 years old."


def test_conditionals_render_admin_branch(
    tera_instance: PyTera,
    admin_user: dict[str, object],
) -> None:
    result = tera_instance.render_template("conditionals.html", user=admin_user)

    assert "Welcome, Administrator Bob!" in result
    assert "Hello, Bob!" not in result


def test_conditionals_render_regular_branch(
    tera_instance: PyTera,
    regular_user: dict[str, object],
) -> None:
    result = tera_instance.render_template("conditionals.html", user=regular_user)

    assert "Hello, Charlie!" in result
    assert "Administrator" not in result


def test_loops_round_prices(
    tera_instance: PyTera,
    inventory_items: list[dict[str, float]],
) -> None:
    result = tera_instance.render_template("loops.html", items=inventory_items)

    assert "<li>Apple: 1.23</li>" in result
    assert "<li>Banana: 0.57</li>" in result
    assert "<li>Orange: 2.89</li>" in result


def test_loops_handle_empty_iterable(tera_instance: PyTera) -> None:
    result = tera_instance.render_template("loops.html", items=[])

    assert "<ul>" in result
    assert "</ul>" in result
    assert "<li>" not in result


def test_filters_apply_builtin_filters(
    tera_instance: PyTera,
    filter_context: dict[str, object],
) -> None:
    result = tera_instance.render_template("filters.html", **filter_context)
    unescaped = html.unescape(html.unescape(result))

    assert "<p>Uppercase: HELLO WORLD</p>" in result
    assert "<p>Length: 11</p>" in result
    assert "Default: N/A" in unescaped
    assert "<p>Slice: b, c</p>" in result


def test_template_inheritance_includes_content(
    tera_instance: PyTera,
    site_name: str,
) -> None:
    result = tera_instance.render_template(
        "child.html",
        site_name=site_name,
        user={"name": "David"},
    )

    assert "<title>Home Page</title>" in result
    assert f"<h2>Welcome to {site_name}</h2>" in result
    assert "<p>Hello, David!</p>" in result
    assert "<h1>My Website</h1>" in result


def test_template_inheritance_without_user_suppresses_greeting(
    tera_instance: PyTera,
    site_name: str,
) -> None:
    result = tera_instance.render_template("child.html", site_name=site_name)

    assert "<title>Home Page</title>" in result
    assert f"<h2>Welcome to {site_name}</h2>" in result
    assert "Hello," not in result


def test_templates_listing_contains_examples(tera_instance: PyTera) -> None:
    templates = set(tera_instance.templates())

    assert {
        "base.html",
        "child.html",
        "basic_variables.html",
        "conditionals.html",
        "filters.html",
        "loops.html",
    }.issubset(templates)


def test_basic_variables_support_unicode(tera_instance: PyTera) -> None:
    result = tera_instance.render_template(
        "basic_variables.html",
        name="测试用户",
        age=25,
    )
    assert "Hello 测试用户! You are 25 years old." == result


def test_basic_variables_accept_none(tera_instance: PyTera) -> None:
    result = tera_instance.render_template(
        "basic_variables.html",
        name=None,
        age=25,
    )
    assert "Hello ! You are 25 years old." == result


def test_multiple_renders_are_isolated(tera_instance: PyTera) -> None:
    first = tera_instance.render_template(
        "basic_variables.html",
        name="Alice",
        age=30,
    )
    second = tera_instance.render_template(
        "basic_variables.html",
        name="Bob",
        age=25,
    )

    assert first != second
    assert second.strip() == "Hello Bob! You are 25 years old."


def test_template_not_found_raises_render_exception(tera_instance: PyTera) -> None:
    with pytest.raises(
        PyTeraRenderException,
        match="Template 'nonexistent.html' not found",
    ):
        tera_instance.render_template("nonexistent.html")
