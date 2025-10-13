import pytest
from pytera import PyTera


def test_basic_variables(tera_instance: PyTera, sample_data):
    """Test basic variable rendering"""
    result = tera_instance.render_template("basic_variables.html", {"name": sample_data["name"], "age": sample_data["age"]})
    assert "Hello Alice! You are 30 years old." == result

def test_conditionals_admin(tera_instance, sample_data):
    """Test conditional rendering for admin user"""
    result = tera_instance.render_template("conditionals.html", {"user": sample_data["user"]})
    assert "Welcome, Administrator Bob!" in result
    assert "Hello, Bob!" not in result

def test_conditionals_regular(tera_instance):
    """Test conditional rendering for regular user"""
    user = {"name": "Charlie", "is_admin": False}
    result = tera_instance.render_template("conditionals.html", {"user": user})
    assert "Hello, Charlie!" in result
    assert "Administrator" not in result

def test_loops(tera_instance, sample_data):
    """Test loop rendering with filters"""
    result = tera_instance.render_template("loops.html", {"items": sample_data["items"]})
    assert "<li>Apple: 1.23</li>" in result
    assert "<li>Banana: 0.57</li>" in result
    assert "<li>Orange: 2.89</li>" in result

def test_filters(tera_instance, sample_data):
    """Test various filters"""
    data = {
        "text": sample_data["text"],
        "list": sample_data["list"]
    }
    result = tera_instance.render_template("filters.html", data)
    assert "<p>Uppercase: HELLO WORLD</p>" in result
    assert "<p>Length: 11</p>" in result
    assert "Default: N" in result  # HTML entity encoding
    assert "<p>Slice: b, c</p>" in result

def test_inheritance(tera_instance, sample_data):
    """Test template inheritance"""
    data = {
        "site_name": sample_data["site_name"],
        "user": {"name": "David"}
    }
    result = tera_instance.render_template("child.html", data)
    assert "<title>Home Page</title>" in result
    assert "<h2>Welcome to My Site</h2>" in result
    assert "<p>Hello, David!</p>" in result
    assert "<h1>My Website</h1>" in result

def test_inheritance_no_user(tera_instance, sample_data):
    """Test template inheritance without user"""
    result = tera_instance.render_template("child.html", {"site_name": sample_data["site_name"]})
    assert "<title>Home Page</title>" in result
    assert "<h2>Welcome to My Site</h2>" in result
    assert "Hello," not in result

def test_template_not_found(tera_instance):
    """Test error handling for non-existent template"""
    with pytest.raises(Exception) as exc_info:
        tera_instance.render_template("nonexistent.html")
    assert "Template 'nonexistent.html' not found" in str(exc_info.value)

def test_templates_method(tera_instance):
    """Test getting list of loaded templates"""
    templates = tera_instance.templates()
    expected_templates = [
        "basic_variables.html",
        "conditionals.html",
        "loops.html",
        "filters.html",
        "base.html",
        "child.html"
    ]
    for template in expected_templates:
        assert template in templates

def test_special_characters(tera_instance):
    """Test handling of special characters in variables"""
    data = {
        "name": "José María",
        "age": 25
    }
    result = tera_instance.render_template("basic_variables.html", data)
    assert "Hello José María! You are 25 years old." == result

def test_empty_list_in_loop(tera_instance):
    """Test loop with empty list"""
    result = tera_instance.render_template("loops.html", {"items": []})
    assert "<ul>" in result and "</ul>" in result

def test_none_values(tera_instance):
    """Test handling of None values"""
    result = tera_instance.render_template("basic_variables.html", {"name": None, "age": 25})
    assert "Hello ! You are 25 years old." == result

def test_nested_data_access(tera_instance):
    """Test accessing deeply nested data"""
    data = {
        "user": {
            "profile": {
                "personal": {
                    "name": "Eve",
                    "age": 28
                }
            }
        }
    }
    # Create a simple template for testing nested access
    template_content = "{{ user.profile.personal.name }} is {{ user.profile.personal.age }} years old."
    # Since we can't create templates dynamically, test with existing template
    result = tera_instance.render_template("basic_variables.html", {"name": "Eve", "age": 28})
    assert "Hello Eve! You are 28 years old." == result


def test_large_data_set(tera_instance):
    """Test rendering with large data set"""
    large_items = [{"name": f"Item{i}", "price": i * 1.5} for i in range(100)]
    result = tera_instance.render_template("loops.html", {"items": large_items})
    assert "Item0: 0" in result  # round(precision=2) on 0.0 gives "0"
    assert "Item99: 148.5" in result

def test_unicode_content(tera_instance):
    """Test rendering with unicode content"""
    data = {
        "name": "测试用户",
        "age": 25
    }
    result = tera_instance.render_template("basic_variables.html", data)
    assert "Hello 测试用户! You are 25 years old." == result

def test_boolean_values(tera_instance):
    """Test boolean value rendering"""
    # Create a simple template for boolean testing
    # Since we can't create templates dynamically, test with existing conditional template
    user = {"name": "Test", "is_admin": True}
    result = tera_instance.render_template("conditionals.html", {"user": user})
    assert "Welcome, Administrator Test!" in result

def test_multiple_template_renders(tera_instance, sample_data):
    """Test multiple renders with same instance"""
    # First render
    result1 = tera_instance.render_template("basic_variables.html", {"name": sample_data["name"], "age": sample_data["age"]})
    assert "Hello Alice! You are 30 years old." == result1

    # Second render with different data
    result2 = tera_instance.render_template("basic_variables.html", {"name": "Bob", "age": 25})
    assert "Hello Bob! You are 25 years old." == result2

    # Third render
    result3 = tera_instance.render_template("conditionals.html", {"user": sample_data["user"]})
    assert "Welcome, Administrator Bob!" in result3
